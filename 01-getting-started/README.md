# 🚀 Getting Started with Microsoft Agent Framework

This section introduces the fundamentals of **Microsoft Agent Framework** and provides the foundation for building AI agents and agentic workflows.

## 🎯 Objectives

By the end of this section, I aim to understand:

- What Microsoft Agent Framework is
- Why an Agent Framework is needed
- What an AI agent is
- How an agent differs from a traditional LLM application
- Core components of an agent
- How agents interact with models and tools
- The basic architecture of Microsoft Agent Framework
- How to set up the development environment
- How to create and run the first agent

---

## 🧠 What is Microsoft Agent Framework?

Microsoft Agent Framework is Microsoft's framework for building **AI agents and agentic workflows**.

It provides building blocks for creating agents that can:

- Reason over user requests
- Interact with Large Language Models (LLMs)
- Use tools and external functions
- Maintain conversation state
- Access knowledge through RAG
- Collaborate with other agents
- Participate in workflows
- Integrate with enterprise systems

---

## 🤖 What is an AI Agent?

**A traditional LLM application generally follows a simple pattern:**

```text
User
  ↓
Application
  ↓
LLM
  ↓
Response

```

**An AI agent can go beyond simply generating a response:**

```text
User
  ↓
Agent
  ↓
Understand the task
  ↓
Reason about the task
  ↓
Select tools / actions
  ↓
Execute actions
  ↓
Evaluate results
  ↓
Respond to the user

```
The key idea is that an agent can **use capabilities and take actions**, rather than only generating text.

# 🏗️ Basic Agent Architecture

**A simplified agent architecture can be represented as:**

                    ┌──────────────┐
                    │     User     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    Agent     │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
           LLM/Model     Tools       Memory
              │            │            │
              └────────────┼────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Response   │
                    └──────────────┘

# 🔍 Agent vs Traditional LLM Application

| Capability             | Traditional LLM App   | AI Agent |
| ---------------------- | --------------------- | -------- |
| Generate text          | ✅                     | ✅        |
| Understand user intent | ✅                     | ✅        |
| Use external tools     | Limited               | ✅        |
| Take actions           | Limited               | ✅        |
| Maintain state         | Application dependent | ✅        |
| Multi-step reasoning   | Limited               | ✅        |
| Work with other agents | ❌                     | ✅        |
| Execute workflows      | Application dependent | ✅        |

**Note:** The boundary between an LLM application and an agent is not always absolute. The important distinction is the ability to use models together with tools, state, and orchestration to accomplish tasks.

# 🧩 Key Concepts

During this tutorial, I will explore the following concepts:

**Agents**

The core building block for creating intelligent applications.

**Tools**

Functions or capabilities that allow an agent to interact with external systems and perform actions.

**Conversations & State**

Mechanisms for maintaining context across interactions.

**Memory**

Ways to provide agents with relevant information from previous interactions or external knowledge.

**RAG**

Retrieval-Augmented Generation allows agents to retrieve relevant information from knowledge sources before generating a response.

**Workflows**

Structured orchestration of multiple steps, agents, and actions.

**Multi-Agent Systems**

Multiple specialized agents collaborating to solve a larger problem.

**Human-in-the-Loop**

Patterns where human intervention or approval is incorporated into an agentic process.

# 🛠️ Technology Stack

**This tutorial will primarily use:**

* Microsoft Agent Framework
* Python
* Microsoft Azure
* Azure AI / Microsoft Foundry
* Large Language Models
* RAG
* REST APIs

# 🗺️ Learning Path

```text
Getting Started
      ↓
First Agent
      ↓
Tools
      ↓
Multi-Turn Conversations
      ↓
Memory & Persistence
      ↓
RAG
      ↓
Middleware
      ↓
Agents as Tools
      ↓
Workflows
      ↓
Multi-Agent Systems
      ↓
Human-in-the-Loop
      ↓
Evaluation & Tracing
      ↓
Hosting
      ↓
Enterprise Agent Architecture
```

# 📚 Official Documentation

For the latest concepts and APIs, refer to the official Microsoft Agent Framework documentation.

* [Microsoft Agent Framework Documentation](https://learn.microsoft.com/en-us/agent-framework/overview/?pivots=programming-language-python)
* [Microsoft Agent Framework GitHub Repository](https://github.com/microsoft/agent-framework)
* [Microsoft Agent Framework Samples](https://github.com/microsoft/agent-framework-samples)

# 📝 Learning Notes

For each topic in this repository, I will document:

* **Concept** – What is it?
* **Why** – Why is it needed?
* **Architecture** – How does it work?
* **Implementation** – How can it be built?
* **Execution** – What happens when it runs?
* **Observations** – What did I learn?
* **Use Cases** – Where can it be applied?
* **Enterprise Perspective** – How can it be used in real-world solutions?

# ⚠️ Disclaimer

This is an independent learning project created for educational purposes.

No proprietary or confidential information from employers or clients is included in this repository.
