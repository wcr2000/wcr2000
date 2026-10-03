<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/wcr2000/wcr2000/output/banner-night.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/wcr2000/wcr2000/output/banner-day.svg">
    <img src="https://raw.githubusercontent.com/wcr2000/wcr2000/output/banner-day.svg" width="100%" alt="Watchara “First”, AI engineer and automation builder, with live contribution stats">
  </picture>
</p>

I build AI that does real work: reading handwritten slips, catching fraud before the money is gone, and moving data between systems that were never meant to talk to each other. I also teach people in Thailand to build their own AI employees under **AI พารวย**. Mostly Python and TypeScript, with a Rust game on the side.

![Python](https://img.shields.io/badge/Python-2f6f73?style=flat-square&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-1f2430?style=flat-square&logo=typescript&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-2f6f73?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-1f2430?style=flat-square&logo=postgresql&logoColor=white)
![n8n](https://img.shields.io/badge/n8n-e8743b?style=flat-square&logo=n8n&logoColor=white)
![Odoo](https://img.shields.io/badge/Odoo-7b7f8a?style=flat-square&logo=odoo&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2f6f73?style=flat-square&logo=docker&logoColor=white)
![Rust](https://img.shields.io/badge/Rust-1f2430?style=flat-square&logo=rust&logoColor=white)
![Claude Code](https://img.shields.io/badge/Claude_Code-e8743b?style=flat-square&logo=anthropic&logoColor=white)

[AI agents & teaching](#ai-agents--teaching) · [Document AI & vision](#document-ai--vision) · [Platforms & data](#platforms--data) · [Side quests](#side-quests) · [The AI Factory](#meanwhile-on-the-factory-floor)

## AI agents & teaching

<table width="100%">
  <tr>
    <td width="50%" valign="top">
      <h3><img src="images/icons/teach.svg" width="28" height="28" alt=""> <a href="https://github.com/wcr2000/hermes-agent-live-course">Hermes Agent Live Course</a></h3>
      <p>Build an AI employee in five evenings. The hands-on companion to my live course goes from agent basics through memory, tools, skills, MCP and multi-agent teams. You finish with an AI employee running on your real work.</p>
      <p><sub>Agent → Memory → Tools → Skills → MCP → Workflow → Multi-agent</sub></p>
    </td>
    <td width="50%" valign="top">
      <h3><img src="images/icons/agent.svg" width="28" height="28" alt=""> <a href="https://github.com/wcr2000/skill-private-marketing-agency-tutorial">Private Marketing Agency</a></h3>
      <p>A week of marketing content from one command. Eight connected agents inside Claude Code handle research, planning, writing in your brand voice, design and scheduling. No coding required.</p>
      <p><sub>Claude Code · Skills · 8 agents · about 2.5 hours to build</sub></p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3><img src="images/icons/teach.svg" width="28" height="28" alt=""> <a href="https://github.com/wcr2000/ai-content-slide">AI Working</a></h3>
      <p>A one-hour beginner course on creating social content with AI: captions, images, a month's content plan, and video scripts. Every part ships with ready-to-use prompts.</p>
    </td>
    <td width="50%" valign="top">
      <h3><img src="images/icons/graph.svg" width="28" height="28" alt=""> <a href="https://github.com/wcr2000/ai-rag">RAG starter</a></h3>
      <p>Retrieval-augmented generation without the magic. Load PDFs and text, chunk them, embed them into FAISS, and answer questions with the sources in context. Usable from the CLI or a FastAPI endpoint.</p>
    </td>
  </tr>
</table>

## Document AI & vision

<table width="100%">
  <tr>
    <td width="50%" valign="top">
      <h3><img src="images/icons/document.svg" width="28" height="28" alt=""> Handwritten slip OCR <img src="https://img.shields.io/badge/private-2f2f2f?style=flat-square" alt="private"></h3>
      <p>Photograph a handwritten parking slip and an LLM reads it. A person confirms the reading, and it's saved to Postgres. When the owner comes back, fuzzy search finds the record even with a misspelt name or a wrong digit.</p>
      <p><sub>FastAPI · OpenRouter · Postgres · human in the loop</sub></p>
    </td>
    <td width="50%" valign="top">
      <h3><img src="images/icons/document.svg" width="28" height="28" alt=""> <a href="https://github.com/wcr2000/ocr-guide">OCR Guide (Thai focus)</a></h3>
      <p>Everything I wish I'd had before an OCR hackathon: preprocessing, PDF-to-text, scanned versus digital documents, and pipelines from PDF to image to CSV with quality checks. Written for Thai text.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3><img src="images/icons/eye.svg" width="28" height="28" alt=""> <a href="https://github.com/wcr2000/License-Plate-Recognition-Lab">License Plate Recognition Lab</a></h3>
      <p>Thai license plate detection and reading with YOLOv8 and YOLOv11, from notebook experiments to a service that pulls data from ID cards and plates.</p>
    </td>
    <td width="50%" valign="top">
      <h3><img src="images/icons/mic.svg" width="28" height="28" alt=""> <a href="https://github.com/wcr2000/speech-to-text-whisper">Speech-to-text with Whisper</a></h3>
      <p>Drop an audio file in a folder and get a Thai transcript back. A background service watches the folder, runs Whisper, and works with n8n through polling. Handles m4a, mp3, wav and seven other formats.</p>
    </td>
  </tr>
</table>

## Platforms & data

<table width="100%">
  <tr>
    <td width="50%" valign="top">
      <h3><img src="images/icons/gateway.svg" width="28" height="28" alt=""> SentraAI Gateway <img src="https://img.shields.io/badge/private-2f2f2f?style=flat-square" alt="private"></h3>
      <p>One OpenAI-compatible endpoint for OpenAI, Anthropic and Google, tracking token usage and cost per model. It's built to comply with Thailand's PDPA, and a Next.js dashboard shows where the money goes.</p>
      <p><sub>FastAPI · Next.js · streaming · PDPA</sub></p>
    </td>
    <td width="50%" valign="top">
      <h3><img src="images/icons/graph.svg" width="28" height="28" alt=""> Fraud Intelligence <img src="https://img.shields.io/badge/private-2f2f2f?style=flat-square" alt="private"></h3>
      <p>Catch fraud earlier than rule-based systems by following the money as a graph. It visualizes money trails, explains each risk signal in plain language, and estimates how much can still be recovered.</p>
      <p><sub>NetworkX · FastAPI · React · Cytoscape.js</sub></p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3><img src="images/icons/database.svg" width="28" height="28" alt=""> Logistics data warehouse <img src="https://img.shields.io/badge/client_work-2f2f2f?style=flat-square" alt="client work"></h3>
      <p>A reporting warehouse built from several source databases: 60+ tables, monthly partitions and materialized views. It backfilled over 30 million shipments with SLA calculations and feeds BI dashboards directly.</p>
      <p><sub>PostgreSQL · ETL · partitioning · BI</sub></p>
    </td>
    <td width="50%" valign="top">
      <h3><img src="images/icons/puzzle.svg" width="28" height="28" alt=""> ERP sync &amp; automation <img src="https://img.shields.io/badge/client_work-2f2f2f?style=flat-square" alt="client work"></h3>
      <p>Keeps master data consistent between head office and branches through Kafka and custom Odoo modules. Repetitive business work runs as n8n workflows.</p>
      <p><sub>Odoo · Kafka · n8n · Docker</sub></p>
    </td>
  </tr>
</table>

## Side quests

<table width="100%">
  <tr>
    <td width="50%" valign="top">
      <h3><img src="images/icons/puzzle.svg" width="28" height="28" alt=""> <a href="https://github.com/wcr2000/dom-manipulation-image-preview">n8n Image Preview</a></h3>
      <p>A Chrome extension that turns image URLs in n8n Data Tables into real thumbnails. Hover to enlarge, click to open, and it keeps up with dynamic content.</p>
    </td>
    <td width="50%" valign="top">
      <h3><img src="images/icons/game.svg" width="28" height="28" alt=""> AI Living World <img src="https://img.shields.io/badge/in_progress-e8743b?style=flat-square" alt="in progress"></h3>
      <p>Game AI that's more than a scripted NPC. An experiment in Rust where characters have their own needs, memories and plans.</p>
    </td>
  </tr>
</table>

---

<div align="center">
  <h3 id="meanwhile-on-the-factory-floor">Meanwhile, on the factory floor...</h3>
  <p><sub>Every day of contributions becomes a crate on the belt. The robot arms stamp them, and the gauge keeps the streak honest. Redrawn every few hours by a GitHub Action.</sub></p>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/wcr2000/wcr2000/output/factory-night.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/wcr2000/wcr2000/output/factory-day.svg">
    <img src="https://raw.githubusercontent.com/wcr2000/wcr2000/output/factory-day.svg" width="100%" alt="The AI Factory: the last 14 days of contributions ride a conveyor belt past two robot arms, beside a streak gauge">
  </picture>
  <p><sub>☕ Fuelled by ชาไทย</sub></p>
</div>
