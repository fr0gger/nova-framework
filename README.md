# NOVA: The Prompt Pattern Matching

![GitHub](https://img.shields.io/github/fr0gger/nova-framework)

<p align="center">
    <img src="nova_doc/docs/nova.svg" alt="NOVA Logo">
</p>

Generative AI systems are rapidly being adopted and deployed across organizations. While they enhance productivity and efficiency, they also expand the attack surface.

How do you detect abusive usage of your system? How do you hunt for malicious prompts? Whether it is identifying jailbreaking attempts, preventing reputational damage, or spotting unexpected behaviors, tracking prompt TTPs can be very useful to track the usage of your AI systems.

That's where NOVA comes in!

🚧 **Disclaimer:** NOVA is currently in beta. Expect potential bugs, incomplete features, and ongoing improvements. If you identify a bug, please [report it here](https://github.com/fr0gger/nova-framework/issues).

NOVA is an open-source prompt pattern matching system combining keyword detection, semantic similarity, and LLM-based evaluation to analyze and detect prompt content.

## Features

- 🔍 **Keyword Detection:** Flag suspicious prompts using predefined keywords or regex.
- 💬 **Semantic Similarity:** Identify pattern variations using configurable thresholds.
- ✨ **LLM Matching:** Create matching rules using natural language evaluated by LLM.

Inspired by YARA syntax, NOVA rules are readable and flexible, ideal for prompt hunting and threat detection.

## Anatomy of a NOVA Rule

```bash
rule RuleName
{
    meta:
        description = "Rule description"
        author = "Author name"

    keywords:
        $keyword1 = "exact text"
        $keyword2 = /regex pattern/i

    semantics:
        $semantic1 = "semantic pattern" (0.6)

    llm:
        $llm_check = "LLM evaluation prompt" (0.7)

    condition:
        keywords.$keyword1 or semantics.$semantic1 or llm.$llm_check
}
```

## Getting Started

```bash
pip install nova-framework
```

## License

This project is licensed under the [MIT License](LICENSE).

## Credits

Created and maintained by [fr0gger](https://github.com/fr0gger).