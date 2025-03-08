"""
NOVA: The Prompt Pattern Matching
Author: Thomas Roccia 
twitter: @fr0gger_
License: MIT License
Version: 1.0.0
Description: LLM-based evaluator implementations
"""

import os
import json
import requests
import re
from typing import Dict, List, Optional, Tuple, Any, Union
from nova.evaluators.base import LLMEvaluator


class OpenAIEvaluator(LLMEvaluator):
    """
    LLM evaluator using OpenAI's API.
    Evaluates prompts using various OpenAI models.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize the LLM evaluator with API credentials.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY environment variable)
            model: OpenAI model to use
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
        self.base_url = "https://api.openai.com/v1/chat/completions"
        
        # Validate API key
        if not self.api_key:
            print("Warning: No API key provided for OpenAI LLM evaluator. Set OPENAI_API_KEY environment variable or pass api_key.")
    
    def evaluate(self, pattern: str, text: str) -> Union[bool, Tuple[bool, float]]:
        """
        Basic evaluate implementation for the BaseEvaluator interface.
        
        Args:
            pattern: The pattern to evaluate
            text: The text to check
            
        Returns:
            Boolean indicating match or tuple of (matched, confidence)
        """
        matched, confidence, _ = self.evaluate_prompt(pattern, text)
        return matched, confidence
    
    def evaluate_prompt(self, prompt_template: str, text: str, temperature: float = 0.1) -> Tuple[bool, float, Dict[str, Any]]:
        """
        Evaluate a text using the provided prompt template with OpenAI API.
        
        Args:
            prompt_template: The prompt to send to the LLM
            text: The text to evaluate
            temperature: Temperature setting for the model (0.0-1.0)
            
        Returns:
            Tuple of (matched, confidence, details)
        """
        if not self.api_key:
            # No API key available
            return False, 0.0, {"error": "No API key available"}
        
        try:
            # Format the complete prompt
            full_prompt = (
                f"{prompt_template}\n\n"
                f"Text to evaluate: {text}\n\n"
                f"Respond with a JSON object with keys: matched (boolean), confidence (float 0-1), reason (string)"
            )
            
            # Call the OpenAI API
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system", 
                            "content": "You are a helpful assistant that evaluates text based on the given criteria. "
                                      "Respond with a JSON object containing 'matched' (boolean), 'confidence' (float 0-1), "
                                      "and 'reason' (string)."
                        },
                        {"role": "user", "content": full_prompt}
                    ],
                    "temperature": temperature,  # Use the provided temperature
                    "response_format": {"type": "json_object"}
                },
                timeout=10  # Add timeout for network operations
            )
            
            # Process the response
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "{}")
                
                # Parse the JSON response
                try:
                    evaluation = json.loads(content)
                    matched = bool(evaluation.get("matched", False))
                    confidence = float(evaluation.get("confidence", 0.0))
                    
                    # Add additional info to the result
                    evaluation["model"] = self.model
                    evaluation["api_status"] = "success"
                    evaluation["evaluator_type"] = "openai"
                    evaluation["temperature"] = temperature  # Include the temperature used
                    
                    return matched, confidence, evaluation
                except json.JSONDecodeError:
                    print(f"Failed to parse LLM response: {content}")
                    return False, 0.0, {"error": "Invalid response format", "raw_content": content}
            else:
                error_msg = f"API error: {response.status_code}, {response.text}"
                print(error_msg)
                return False, 0.0, {"error": error_msg, "status_code": response.status_code}
        
        except requests.Timeout:
            error_msg = "API request timed out"
            print(error_msg)
            return False, 0.0, {"error": error_msg}
            
        except Exception as e:
            error_msg = f"Error in LLM evaluation: {str(e)}"
            print(error_msg)
            return False, 0.0, {"error": error_msg}


class AnthropicEvaluator(LLMEvaluator):
    """
    LLM evaluator using Anthropic's Claude API.
    Evaluates prompts using Claude models.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-sonnet-20240229"):
        """
        Initialize the Claude LLM evaluator.
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY environment variable)
            model: Anthropic model to use
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.model = model
        self.base_url = "https://api.anthropic.com/v1/messages"
        
        # Validate API key
        if not self.api_key:
            print("Warning: No API key provided for Anthropic LLM evaluator. Set ANTHROPIC_API_KEY environment variable or pass api_key.")
    
    def evaluate(self, pattern: str, text: str) -> Union[bool, Tuple[bool, float]]:
        """
        Basic evaluate implementation for the BaseEvaluator interface.
        
        Args:
            pattern: The pattern to evaluate
            text: The text to check
            
        Returns:
            Boolean indicating match or tuple of (matched, confidence)
        """
        matched, confidence, _ = self.evaluate_prompt(pattern, text)
        return matched, confidence
    
    def evaluate_prompt(self, prompt_template: str, text: str, temperature: float = 0.1) -> Tuple[bool, float, Dict[str, Any]]:
        """
        Evaluate a text using the provided prompt template with Anthropic API.
        
        Args:
            prompt_template: The prompt to send to the LLM
            text: The text to evaluate
            temperature: Temperature setting for the model (0.0-1.0)
            
        Returns:
            Tuple of (matched, confidence, details)
        """
        if not self.api_key:
            # No API key available
            return False, 0.0, {"error": "No API key available"}
        
        try:
            # Format the complete prompt
            system_prompt = (
                "You evaluate text based on given criteria. "
                "Respond with a JSON object containing 'matched' (boolean), "
                "'confidence' (float 0-1), and 'reason' (string)."
            )
            
            user_prompt = (
                f"{prompt_template}\n\n"
                f"Text to evaluate: {text}\n\n"
                f"Respond with a JSON object with keys: matched (boolean), confidence (float 0-1), reason (string)"
            )
            
            # Call the Anthropic API
            response = requests.post(
                self.base_url,
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                },
                json={
                    "model": self.model,
                    "system": system_prompt,
                    "messages": [
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": temperature,  # Use the provided temperature
                    "max_tokens": 200
                },
                timeout=15  # Longer timeout for Anthropic API
            )
            
            # Process the response
            if response.status_code == 200:
                result = response.json()
                content = result.get("content", [{}])[0].get("text", "{}")
                
                # Parse the JSON response
                try:
                    # Find JSON in response (Claude might add text before/after)
                    json_start = content.find('{')
                    json_end = content.rfind('}') + 1
                    
                    if json_start >= 0 and json_end > json_start:
                        json_content = content[json_start:json_end]
                        evaluation = json.loads(json_content)
                        matched = bool(evaluation.get("matched", False))
                        confidence = float(evaluation.get("confidence", 0.0))
                        
                        # Add additional info to the result
                        evaluation["model"] = self.model
                        evaluation["api_status"] = "success"
                        evaluation["evaluator_type"] = "anthropic"
                        evaluation["temperature"] = temperature  # Include the temperature used
                        
                        return matched, confidence, evaluation
                    else:
                        return False, 0.0, {"error": "No JSON found in response", "raw_content": content}
                except json.JSONDecodeError:
                    print(f"Failed to parse Claude response: {content}")
                    return False, 0.0, {"error": "Invalid response format", "raw_content": content}
            else:
                error_msg = f"API error: {response.status_code}, {response.text}"
                print(error_msg)
                return False, 0.0, {"error": error_msg, "status_code": response.status_code}
        
        except requests.Timeout:
            error_msg = "API request timed out"
            print(error_msg)
            return False, 0.0, {"error": error_msg}
            
        except Exception as e:
            error_msg = f"Error in LLM evaluation: {str(e)}"
            print(error_msg)
            return False, 0.0, {"error": error_msg}


class AzureOpenAIEvaluator(OpenAIEvaluator):
    """
    LLM evaluator using Azure OpenAI Service.
    Extends OpenAIEvaluator with Azure-specific configuration.
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        endpoint: Optional[str] = None,
        deployment_name: str = "gpt-35-turbo",
        api_version: str = "2023-05-15"
    ):
        """
        Initialize the Azure OpenAI evaluator.
        
        Args:
            api_key: Azure OpenAI API key (defaults to AZURE_OPENAI_API_KEY environment variable)
            endpoint: Azure OpenAI endpoint (defaults to AZURE_OPENAI_ENDPOINT environment variable)
            deployment_name: Azure deployment name
            api_version: Azure OpenAI API version
        """
        # Use Azure-specific environment variables
        self.api_key = api_key or os.environ.get("AZURE_OPENAI_API_KEY")
        self.endpoint = endpoint or os.environ.get("AZURE_OPENAI_ENDPOINT")
        self.deployment_name = deployment_name
        self.api_version = api_version
        
        # Validate configuration
        if not self.api_key:
            print("Warning: No API key provided for Azure OpenAI evaluator. Set AZURE_OPENAI_API_KEY environment variable or pass api_key.")
        
        if not self.endpoint:
            print("Warning: No endpoint provided for Azure OpenAI evaluator. Set AZURE_OPENAI_ENDPOINT environment variable or pass endpoint.")
        
        # Calculate base URL
        if self.endpoint:
            # Remove trailing slash if present
            endpoint = self.endpoint.rstrip('/')
            self.base_url = f"{endpoint}/openai/deployments/{deployment_name}/chat/completions?api-version={api_version}"
        else:
            self.base_url = None
    
    def evaluate_prompt(self, prompt_template: str, text: str, temperature: float = 0.1) -> Tuple[bool, float, Dict[str, Any]]:
        """
        Evaluate a text using the provided prompt template with Azure OpenAI API.
        
        Args:
            prompt_template: The prompt to send to the LLM
            text: The text to evaluate
            temperature: Temperature setting for the model (0.0-1.0)
            
        Returns:
            Tuple of (matched, confidence, details)
        """
        if not self.api_key or not self.base_url:
            # Missing configuration
            return False, 0.0, {"error": "Missing Azure OpenAI configuration"}
        
        try:
            # Format the complete prompt
            full_prompt = (
                f"{prompt_template}\n\n"
                f"Text to evaluate: {text}\n\n"
                f"Respond with a JSON object with keys: matched (boolean), confidence (float 0-1), reason (string)"
            )
            
            # Call the Azure OpenAI API
            response = requests.post(
                self.base_url,
                headers={
                    "api-key": self.api_key,
                    "Content-Type": "application/json"
                },
                json={
                    "messages": [
                        {
                            "role": "system", 
                            "content": "You are a helpful assistant that evaluates text based on the given criteria. "
                                      "Respond with a JSON object containing 'matched' (boolean), 'confidence' (float 0-1), "
                                      "and 'reason' (string)."
                        },
                        {"role": "user", "content": full_prompt}
                    ],
                    "temperature": temperature,  # Use the provided temperature
                    "response_format": {"type": "json_object"}
                },
                timeout=10
            )
            
            # Process the response (same as OpenAI)
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "{}")
                
                # Parse the JSON response
                try:
                    evaluation = json.loads(content)
                    matched = bool(evaluation.get("matched", False))
                    confidence = float(evaluation.get("confidence", 0.0))
                    
                    # Add additional info to the result
                    evaluation["model"] = self.deployment_name
                    evaluation["api_status"] = "success"
                    evaluation["evaluator_type"] = "azure"
                    evaluation["temperature"] = temperature  # Include the temperature used
                    
                    return matched, confidence, evaluation
                except json.JSONDecodeError:
                    print(f"Failed to parse Azure OpenAI response: {content}")
                    return False, 0.0, {"error": "Invalid response format", "raw_content": content}
            else:
                error_msg = f"API error: {response.status_code}, {response.text}"
                print(error_msg)
                return False, 0.0, {"error": error_msg, "status_code": response.status_code}
                
        except Exception as e:
            error_msg = f"Error in Azure OpenAI evaluation: {str(e)}"
            print(error_msg)
            return False, 0.0, {"error": error_msg}


class OllamaEvaluator(LLMEvaluator):
    """
    LLM evaluator using local Ollama models.
    Evaluates prompts using models run through Ollama API.
    """
    
    def __init__(self, 
                 host: Optional[str] = None,
                 model: str = "llama3",
                 timeout: int = 30,
                 debug: bool = True):
        """
        Initialize the Ollama LLM evaluator.
        
        Args:
            host: Ollama host URL (defaults to OLLAMA_HOST environment variable or http://localhost:11434)
            model: Ollama model to use (defaults to llama3)
            timeout: Timeout in seconds for API calls
            debug: Enable debug output
        """
        self.host = host or os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        self.model = model
        self.timeout = timeout
        self.debug = debug
        
        # Remove trailing slash if present
        self.host = self.host.rstrip('/')
        self.base_url = f"{self.host}/api/chat"
        
        # Validate host
        if not self.host:
            print("Warning: No host provided for Ollama LLM evaluator. Set OLLAMA_HOST environment variable or pass host.")
    
    def evaluate(self, pattern: str, text: str) -> Union[bool, Tuple[bool, float]]:
        """
        Basic evaluate implementation for the BaseEvaluator interface.
        
        Args:
            pattern: The pattern to evaluate
            text: The text to check
            
        Returns:
            Boolean indicating match or tuple of (matched, confidence)
        """
        matched, confidence, _ = self.evaluate_prompt(pattern, text)
        return matched, confidence
    
    def _debug_print(self, message, data=None):
        """Print debug information if debug mode is enabled."""
        if self.debug:
            #print(f"[OLLAMA DEBUG] {message}")
            if data is not None:
                if isinstance(data, str) and len(data) > 500:
                    # For long strings, print a summary
                    #print(f"[OLLAMA DEBUG] Content (first 200 chars): {data[:200]}")
                    #print(f"[OLLAMA DEBUG] Content (last 200 chars): {data[-200:]}")
                    #print(f"[OLLAMA DEBUG] Content length: {len(data)}")
                    # Print line by line for the first few lines to see structure
                    lines = data.split('\n')
                    #for i, line in enumerate(lines[:5]):
                        #print(f"[OLLAMA DEBUG] Line {i+1} ({len(line)} chars): {line}")
                #else:
                #    print(f"[OLLAMA DEBUG] {data}")
                pass
    
    def _extract_response_from_streaming_json(self, response_text):
        """
        Extract complete response from streaming JSON format.
        Each line is a separate JSON object with a piece of the final content.
        """
        self._debug_print("Processing streaming response format")
        
        # Split the response into lines
        lines = response_text.strip().split('\n')
        self._debug_print(f"Found {len(lines)} response chunks")
        
        # Collect all content pieces
        full_content = ""
        
        for i, line in enumerate(lines):
            try:
                # Parse each line as a separate JSON object
                chunk = json.loads(line)
                
                # Extract the content from this chunk
                content_piece = chunk.get("message", {}).get("content", "")
                full_content += content_piece
                
                # If this is the last chunk and has done=true, note it
                if chunk.get("done", False) and i == len(lines) - 1:
                    self._debug_print("Found final chunk with done=true")
            except json.JSONDecodeError:
                self._debug_print(f"Failed to parse chunk {i+1} as JSON")
                continue
        
        self._debug_print(f"Reconstructed full content: {full_content}")
        return full_content
    
    def _extract_response_fields(self, content):
        """
        Extract key fields from response content using regex patterns.
        This is used when JSON parsing fails.
        """
        self._debug_print("Attempting to extract fields using regex")
        
        # Try to find matched value from text
        matched_pattern = r'"matched"\s*:\s*(true|false)'
        confidence_pattern = r'"confidence"\s*:\s*([0-9.]+)'
        reason_pattern = r'"reason"\s*:\s*"([^"]*)"'
        
        matched_match = re.search(matched_pattern, content, re.IGNORECASE)
        confidence_match = re.search(confidence_pattern, content)
        reason_match = re.search(reason_pattern, content)
        
        # Set default values
        matched = False
        confidence = 0.5
        reason = "Manually extracted from response"
        
        # Update with extracted values if found
        if matched_match:
            matched = matched_match.group(1).lower() == 'true'
            self._debug_print(f"Found matched = {matched}")
        else:
            # Try to infer from text
            lower_content = content.lower()
            if "yes" in lower_content or "true" in lower_content or "match" in lower_content:
                matched = True
                self._debug_print(f"Inferred matched = {matched}")
        
        if confidence_match:
            try:
                confidence = float(confidence_match.group(1))
                if confidence < 0 or confidence > 1:
                    confidence = max(0, min(confidence, 1))  # Clamp to 0-1 range
                self._debug_print(f"Found confidence = {confidence}")
            except:
                pass
        
        if reason_match:
            reason = reason_match.group(1)
            self._debug_print(f"Found reason = {reason}")
        
        return {
            "matched": matched,
            "confidence": confidence,
            "reason": reason,
            "evaluator_type": "ollama",
            "extraction_method": "regex",
            "raw_content": content[:100] + ("..." if len(content) > 100 else "")
        }
    
    def evaluate_prompt(self, prompt_template: str, text: str, temperature: float = 0.1) -> Tuple[bool, float, Dict[str, Any]]:
        """
        Evaluate a text using the provided prompt template with Ollama API.
        
        Args:
            prompt_template: The prompt to send to the LLM
            text: The text to evaluate
            temperature: Temperature setting for the model (0.0-1.0)
            
        Returns:
            Tuple of (matched, confidence, details)
        """
        try:
            # Format the complete prompt
            system_prompt = (
                "You evaluate text based on given criteria. "
                "Respond with ONLY a JSON object containing 'matched' (boolean), "
                "'confidence' (float 0-1), and 'reason' (string). "
                "Format your response as a JSON object and nothing else. "
                "Do not add any explanation before or after the JSON."
            )
            
            user_prompt = (
                f"{prompt_template}\n\n"
                f"Text to evaluate: {text}\n\n"
                f"IMPORTANT: Respond with ONLY a JSON object with these exact keys: matched (boolean), confidence (float 0-1), reason (string)"
            )
            
            self._debug_print("Sending request to Ollama API")
            
            # Call the Ollama API
            response = requests.post(
                self.base_url,
                headers={"Content-Type": "application/json"},
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "options": {
                        "temperature": temperature  # Use the provided temperature
                    },
                    "stream": False  # Explicitly disable streaming
                },
                timeout=self.timeout
            )
            
            # Process the response
            if response.status_code == 200:
                self._debug_print("Received 200 response from Ollama API")
                
                # First, check if we're dealing with streaming JSON response
                response_text = response.text
                self._debug_print("Raw response text:", response_text)
                
                if '\n' in response_text and response_text.strip().startswith('{"model":'):
                    # This appears to be a streaming response, reconstruct it
                    full_content = self._extract_response_from_streaming_json(response_text)
                    
                    # Try to parse the reconstructed content as JSON
                    try:
                        result_json = json.loads(full_content)
                        self._debug_print("Successfully parsed reconstructed content as JSON")
                        
                        if "matched" in result_json:
                            matched = bool(result_json.get("matched", False))
                            confidence = float(result_json.get("confidence", 0.5))
                            
                            result_json["model"] = self.model
                            result_json["api_status"] = "success"
                            result_json["evaluator_type"] = "ollama"
                            result_json["extraction_method"] = "streaming_reconstruct"
                            result_json["temperature"] = temperature  # Include the temperature used
                            
                            return matched, confidence, result_json
                    except json.JSONDecodeError:
                        self._debug_print("Reconstructed content is not valid JSON, using regex fallback")
                    
                    # If JSON parsing failed, use regex fallback
                    extraction = self._extract_response_fields(full_content)
                    extraction["model"] = self.model
                    extraction["api_status"] = "partial"
                    extraction["temperature"] = temperature  # Include the temperature used
                    
                    return extraction["matched"], extraction["confidence"], extraction
                else:
                    # Not a streaming response, try to parse as regular JSON
                    try:
                        result = json.loads(response_text)
                        content = result.get("message", {}).get("content", "{}")
                        self._debug_print("Content from regular JSON response:", content)
                        
                        try:
                            # Try to parse the content as JSON
                            content_json = json.loads(content)
                            if "matched" in content_json:
                                matched = bool(content_json.get("matched", False))
                                confidence = float(content_json.get("confidence", 0.5))
                                
                                content_json["model"] = self.model
                                content_json["api_status"] = "success"
                                content_json["evaluator_type"] = "ollama"
                                content_json["extraction_method"] = "regular_json"
                                content_json["temperature"] = temperature  # Include the temperature used
                                
                                return matched, confidence, content_json
                        except json.JSONDecodeError:
                            self._debug_print("Content is not valid JSON, using regex fallback")
                        
                        # If JSON parsing failed, use regex fallback
                        extraction = self._extract_response_fields(content)
                        extraction["model"] = self.model
                        extraction["api_status"] = "partial"
                        extraction["temperature"] = temperature  # Include the temperature used
                        
                        return extraction["matched"], extraction["confidence"], extraction
                    except json.JSONDecodeError:
                        self._debug_print("Response is not valid JSON, using regex fallback on raw response")
                        
                        # Direct extraction from raw response
                        extraction = self._extract_response_fields(response_text)
                        extraction["model"] = self.model
                        extraction["api_status"] = "partial"
                        extraction["temperature"] = temperature  # Include the temperature used
                        
                        return extraction["matched"], extraction["confidence"], extraction
            else:
                error_msg = f"API error: {response.status_code}, {response.text}"
                self._debug_print(error_msg)
                return False, 0.0, {"error": error_msg, "status_code": response.status_code, "evaluator_type": "ollama"}
        
        except requests.Timeout:
            error_msg = "API request timed out"
            self._debug_print(error_msg)
            return False, 0.0, {"error": error_msg, "evaluator_type": "ollama"}
            
        except Exception as e:
            error_msg = f"Error in Ollama evaluation: {str(e)}"
            self._debug_print(f"Exception: {type(e).__name__} - {str(e)}")
            import traceback
            self._debug_print(f"Traceback: {traceback.format_exc()}")
            return False, 0.0, {"error": error_msg, "evaluator_type": "ollama"}


def get_validated_evaluator(llm_type: str, model: Optional[str] = None, verbose: bool = False) -> Optional[LLMEvaluator]:
    """
    Get a validated LLM evaluator with proper API key checking and no fallback logic.
    If the requested evaluator can't be created, raises an exception.
    
    Args:
        llm_type: Type of LLM evaluator ('openai', 'anthropic', 'azure', or 'ollama')
        model: Optional model name to use
        verbose: Whether to print verbose information
        
    Returns:
        An LLM evaluator instance or raises an exception if it cannot be created
        
    Raises:
        ValueError: If the required API keys or configuration are not available
    """
    # Initialize variables for selected evaluator
    selected_model = None
    
    # Handle the requested evaluator without fallbacks
    if llm_type.lower() == 'anthropic':
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if api_key:
            selected_model = model or "claude-3-sonnet-20240229"
            if verbose:
                print(f"✓ Using Anthropic evaluator with model: {selected_model}")
            return AnthropicEvaluator(api_key=api_key, model=selected_model)
        else:
            raise ValueError("ANTHROPIC_API_KEY not set in environment variables. Cannot use Anthropic evaluator.")
    
    elif llm_type.lower() == 'azure':
        api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        if api_key and endpoint:
            deployment = model or "gpt-35-turbo"
            if verbose:
                print(f"✓ Using Azure OpenAI evaluator with deployment: {deployment}")
            return AzureOpenAIEvaluator(api_key=api_key, endpoint=endpoint, deployment_name=deployment)
        else:
            missing = []
            if not api_key:
                missing.append("AZURE_OPENAI_API_KEY")
            if not endpoint:
                missing.append("AZURE_OPENAI_ENDPOINT")
            raise ValueError(f"Required environment variables not set: {', '.join(missing)}. Cannot use Azure evaluator.")
    
    elif llm_type.lower() == 'ollama':
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        selected_model = model or "llama3"
        try:
            # Try a simple ping to see if Ollama is running
            requests.get(f"{host}/api/tags", timeout=2)
            if verbose:
                print(f"✓ Using Ollama evaluator with model: {selected_model}")
            return OllamaEvaluator(host=host, model=selected_model)
        except (requests.ConnectionError, requests.Timeout):
            raise ValueError(f"Could not connect to Ollama at {host}. Ensure Ollama service is running.")
    
    elif llm_type.lower() == 'openai':
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            selected_model = model or "gpt-4o-mini"
            if verbose:
                print(f"✓ Using OpenAI evaluator with model: {selected_model}")
            return OpenAIEvaluator(api_key=api_key, model=selected_model)
        else:
            raise ValueError("OPENAI_API_KEY not set in environment variables. Cannot use OpenAI evaluator.")
    
    else:
        # Invalid LLM type
        raise ValueError(f"Unsupported LLM type: {llm_type}. Supported types are: openai, anthropic, azure, ollama")