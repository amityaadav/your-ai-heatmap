const DOMAINS = [
  {
    d:"Foundations & model internals",
    note:"Strong for a non-ML-engineer — the NVIDIA labs did real work here.",
    t:[
      ["Neural network fundamentals",4,"You didn't stop at 'the loss went down.' You asked what 23.89 signified mathematically and worked through softmax → negative log likelihood. Then you built a visualizer that teaches it to others.","Built: NVIDIA-Deep-Learning-labs digit visualizer · 4-layer PyTorch net with animated activations"],
      ["CNNs & convolution",4,"Full transfer-learning lab: frozen VGG16 feature extractor, custom head, then unfreezing. You diagnosed catastrophic forgetting from the learning rate yourself.","NVIDIA DLI certification · Conv2d parameter semantics · coached Swati through the same lab"],
      ["Backprop & gradients",3,"Correct on exploding gradients and clipping. Conceptually clean, but you've never implemented a training loop from scratch.","Quiz-level fluency · used utils.py training loops rather than writing them"],
      ["Transformer architecture",3,"You can lay out the stack for an audience. It's taught knowledge, not derived knowledge.","Used in BA curriculum · answered advanced-round questions correctly"],
      ["Attention & multi-head attention",3,"You correctly identified that multi-head runs parallel projections capturing different relationship types. That's a real answer, not a guess.","Advanced quiz round, five correct in a row"],
      ["Tokens & tokenization",4,"Core of your restaurant-analogy glossary. You've explained this to thirty people who'd never heard of it.","BA curriculum · comic strip series"],
      ["Context windows",4,"Same — taught, and you reason about it when picking models and sizing prompts.","BA curriculum · model selection conversations"],
      ["Embeddings & vector space",3,"The knowledge-graph vs embeddings conversation showed you actually understand what a 1,536-dim space does and doesn't buy you.","Taught in glossary · applied to incident-triage design"],
      ["Pretraining & next-token prediction",3,"You've walked others through the pipeline from raw corpus to instruction-following assistant.","AI timeline conversation"],
      ["RLHF & alignment training",2,"You've had it explained and can repeat the reward-model → RL loop. You've never touched DPO, constitutional methods, or the tradeoffs.","One conversation, receiving rather than reasoning"],
      ["Sampling params (temperature, top-p)",3,"Basic operational fluency; flagged as too basic for your own comic strips.","Considered and rejected as a teaching topic"],
      ["Hallucination & grounding",3,"Your chosen next comic topic. You frame it well for a business audience.","Teaching pipeline"],
      ["Reasoning models & chain-of-thought",3,"You prompt with it and teach it. The current research on test-time compute and CoT structure hasn't come up.","Curriculum module 3"],
      ["Mixture of Experts",2,"Appeared as a line item when you were comparing open models for local inference. No architectural depth.","Model landscape research"],
      ["Quantization (INT4/INT8/GGUF)",2,"You understand it as a VRAM lever — 2GB per billion params, Q4 to fit a 34B. Not as a quality/latency tradeoff you've measured.","Local hardware research"],
      ["Scaling laws & their limits",2,"Encountered in trend reading. Chinchilla, sub-Chinchilla returns, the compute wall — surface only.","AI trends conversation"],
      ["Open weights & model licensing",3,"You did real work here — leaderboard by SWE-bench, open models as a price-floor hedge. That's an informed position.","Local inference economics study for TRP"],
      ["Model distillation",2,"Named in passing while comparing model families.","Model landscape research"]
    ]
  },
  {
    d:"Training & model adaptation",
    note:"Transfer learning is genuinely strong; the LLM-adaptation half is nearly blank.",
    t:[
      ["Transfer learning",4,"Freeze, train, unfreeze, drop the LR, watch for forgetting. You've done the full cycle and taught it.","VGG16 fruit classifier · diagnosed 1e-4 → 1e-6 fix"],
      ["Loss functions",3,"You drew the CrossEntropy vs BCEWithLogits distinction precisely — mutual exclusivity, shape contracts, internal softmax vs sigmoid.","Lab 7 debugging"],
      ["Overfitting & regularization",3,"You spotted 97% train / 84% val as overfitting and applied dropout.","Lab 7"],
      ["Data augmentation",3,"Configured the transforms and understood why validation doesn't shuffle.","Lab 7"],
      ["Hyperparameter tuning",3,"Learning-rate intuition specifically. Not systematic search.","Lab 7"],
      ["LLM fine-tuning (SFT)",2,"Discussed as one of three options against RAG and prompting. Never run.","Comic strip topic candidate"],
      ["LoRA / QLoRA / PEFT",2,"Appears in your hardware research as a thing a 3090 can do. That's the whole extent.","GPU build research"],
      ["Synthetic data generation",2,"Listed in your LLM-capabilities framework. No hands-on.","Training deck framework"],
      ["Dataset curation & labeling",1,"Never discussed. You've only used pre-packaged datasets.",""],
      ["Distributed & large-scale training",1,"Never discussed.",""],
      ["Reward modeling & RL post-training",1,"Never discussed beyond the RLHF summary.",""],
      ["Continual learning",1,"Never discussed. Currently one of the loudest 2026 research threads.",""]
    ]
  },
  {
    d:"Retrieval & knowledge systems",
    note:"You explain RAG better than most people who've built it — but you haven't built it.",
    t:[
      ["RAG fundamentals",3,"You teach it and correctly position it against fine-tuning and prompting. You also questioned whether building one was worth it given managed services — a good instinct that has kept you from building one.","Curriculum · Bedrock Knowledge Bases conversation"],
      ["Knowledge graphs & GraphRAG",3,"Your best conceptual conversation in this space. You understood why nearest-neighbour search can't answer 'what upstream services could cause this symptom' and why that pushes toward graph traversal.","Applied directly to incident-triage POC design"],
      ["Chunking strategies",2,"Named as the hard problem. You've never tuned one against a retrieval metric.","Conceptual only"],
      ["Vector databases",2,"Chroma, FAISS, Pinecone, OpenSearch named. None stood up.","Research only"],
      ["Embedding model selection",2,"Mentioned as a lever. No comparison run.","Research only"],
      ["Hybrid search & reranking",2,"Appeared in reading on 2026 RAG practice.","Trends reading"],
      ["Retrieval quality evaluation",1,"This is the specific gap the fluency assessment called out — 'engineered context assembly with retrieval quality measurement.' Still untouched.","Named as a gap, not closed"],
      ["Managed RAG (Bedrock KB)",2,"Researched the build-vs-buy tradeoff. No Bedrock sandbox access to try it.","Blocked by access, not interest"],
      ["Document parsing & extraction",2,"Listed in your capability framework.","Framework only"],
      ["Memory & episodic state design",2,"AgentCore Memory covered in the full-day training. Nothing built on it.","Bedrock AgentCore training"]
    ]
  },
  {
    d:"Agents & orchestration",
    note:"Your strongest technical territory. MCP in particular is genuine teaching depth.",
    t:[
      ["MCP protocol & primitives",4,"You've authored servers across stdio and HTTP transports, built a Splunk MCP server at a hackathon, walked through all seven primitives, and correctly argued that an MCP server needs no underlying API. You teach this.","Splunk MCP · SQLite PoC · CLI project · MCP Inspector debugging"],
      ["LangGraph",4,"Shipped a production multi-agent system on it and can articulate state merging, fan-out/fan-in, reflection loops, and conditional routing without notes.","Celestial newsletter on Lambda · incident-triage POC"],
      ["Agent architecture patterns",3,"Plan/act loops, reflection, critique-driven routing — you designed with these rather than just naming them.","Celestial system design"],
      ["Multi-agent orchestration",3,"Three parallel research agents shipped. But parallel multi-agent execution at scale was flagged as a gap, and the six-agent expense system was n8n, not code.","Shipped small, not large"],
      ["Tool use & function calling",3,"Central to everything you've built. Solid, unremarkable.","Across all agent work"],
      ["LangChain",3,"Actively working through structured tutorials in a local venv, lesson by lesson. In progress, not finished.","Current learning track"],
      ["Agentic coding tools",3,"Heavy daily driver across Claude Code and Kiro — steering files, spec mode, auto-running test suites before deploy.","To-do kanban project · incident-triage POC"],
      ["Claude Code advanced features",2,"Hooks, subagents, headless mode, checkpointing, Agent SDK — you identified all of them as your highest-leverage gaps and then didn't close them. Scored 2/5 on native features despite topping the MCP-authoring axis.","Explicitly named gap, June audit"],
      ["Bedrock AgentCore",2,"Full-day training. Runtime, Memory, Gateway, Identity, Observability — and a sharp Gateway-to-Apigee analogy. Zero hands-on, sandbox blocked.","Training attended, access denied"],
      ["Strands Agents SDK",2,"Understood as model-driven orchestration vs LangGraph's explicit graphs. Never run — this is your company's standard, which makes it the most expensive gap on this board.","Conceptual only"],
      ["No-code agent platforms",3,"Built a six-agent expense tracking system in n8n end to end.","Shipped"],
      ["Human-in-the-loop design",3,"You argue for review gates on risky actions and understand why bounded tasks beat open-ended chat.","Trends conversation, applied thinking"],
      ["Agent identity & permission scoping",2,"You've named agent identity sprawl as a threat. You haven't designed a scoping model.","AMA security prep"],
      ["Agent-to-agent protocols",1,"A2A and the coordination-protocol layer haven't come up.",""],
      ["Long-horizon task execution",2,"Read about 8-hour agent workflows. Your own agents run in minutes.","Trends reading"]
    ]
  },
  {
    d:"Context & interaction engineering",
    note:"Teaching-grade on the prompting side; the engineering discipline underneath is thinner.",
    t:[
      ["Prompt engineering",4,"You designed a six-module curriculum for thirty BAs, built the mental model (briefing a context-blind collaborator), ran a pre-session poll, and the comic landed. This is unambiguously teaching depth.","Delivered to 30 BAs · comic strip series"],
      ["Few-shot & CoT prompting",4,"Module 3 of your own curriculum, with BA-specific applications.","Curriculum"],
      ["System prompt & role design",3,"You use it deliberately and teach RCTFC-style structure.","Curriculum"],
      ["Context engineering",3,"You correctly see it as the successor framing to prompt engineering and picked it as a comic topic. The measured version — assembling context and proving it improved things — isn't there.","Named topic, unmeasured practice"],
      ["Prompt libraries & reuse",3,"Actively building a living library tied to real TRP artifacts. That's the right instinct and it's in flight.","In progress at TRP"],
      ["Structured outputs & schema validation",2,"Called out as a gap: structured output validation with repair loops. Still open.","Named gap"],
      ["Prompt versioning as tested artifacts",2,"Same assessment, same status. Treating prompts as code you regression-test hasn't started.","Named gap"],
      ["Prompt caching & cost optimisation",2,"You reason about token cost at the model-selection level, not the cache level.","Adjacent knowledge"]
    ]
  },
  {
    d:"Evaluation & reliability",
    note:"The single widest gap on this board, and you already know it.",
    t:[
      ["Eval fundamentals & golden datasets",2,"You researched the courses thoroughly — Hamel and Shreya's Maven cohort, the DeepLearning.AI/Arize option — and identified this as the top gap. Research is not the same as having run one.","Gap identified July 2026, unclosed"],
      ["LLM-as-judge",2,"You listed it as a capability in your teaching framework. Never implemented.","Framework only"],
      ["Trace-level observability for agents",2,"Named as a gap: 'every run leaves an inspectable trace.' Your agents don't yet.","Named gap"],
      ["Error analysis & failure taxonomies",2,"You know the method — group failure modes, fix what matters first. Untried.","Course research"],
      ["Regression testing for agents",2,"You built auto-running test suites for deterministic code, which is real. Non-deterministic agent output is a different problem you haven't tackled.","Adjacent skill, not transferred"],
      ["Benchmarks (SWE-bench, agentic evals)",3,"You built a model leaderboard by SWE-bench score as part of the TCO work — you can explain what these measure and where they mislead.","Local inference study"],
      ["Cost & latency benchmarking",3,"Three-year TCO across hardware tiers, ending in a model-routing recommendation rather than a hardware buy. That's a defensible piece of analysis.","TRP local inference study"],
      ["Guardrails & output filtering",2,"Named in your framework and in the security conversations. Nothing implemented.","Conceptual"],
      ["Classical NLP metrics (BLEU/COMET)",2,"One conversation covering BLEU, METEOR, chrF, BERTScore, COMET, MQM. You received it rather than applied it.","Single conversation"],
      ["Uncertainty & calibration",1,"Never discussed.",""]
    ]
  },
  {
    d:"Security, safety & governance",
    note:"Genuinely good threat-model intuition, entirely unvalidated by hands-on testing.",
    t:[
      ["Prompt injection (direct & indirect)",3,"Your best security thinking. You landed on the point that internal agents are more exposed to indirect injection precisely because they ingest trusted internal documents — and you got there partly by arguing against yourself.","AMA prep · red-team agent concept"],
      ["Entitlement flattening in RAG",3,"You raised this specifically. Most people building RAG have never considered it.","AMA prep"],
      ["Shadow AI & agent inventory",3,"You designed a discovery layer for finding undeclared agent deployments. Strong instinct for where the real risk sits.","Agent Security Evaluator concept"],
      ["Deepfake & social engineering threats",3,"Covered as the inbound half of the AI threat picture.","AMA prep"],
      ["Agent red-teaming in practice",2,"You know Garak, PyRIT, Lakera, Mindgard exist and what they do. You've run none of them.","Market research"],
      ["OWASP LLM Top 10 / MITRE ATLAS",2,"Named as the mapping targets for your compliance layer. Not worked through.","Concept design"],
      ["AI regulation — financial services",3,"FINRA's 2026 oversight report, SEC exam priorities, the 40%/44% adoption-vs-validation gap. You cite real numbers, which is rare.","Applied to TRP context repeatedly"],
      ["AI governance frameworks (NIST, ISO 42001)",2,"AIGP identified as your accessible next certification. Frameworks not yet studied.","Certification research"],
      ["EU AI Act & global policy",1,"Hasn't come up. Notable given TRP's global footprint.",""],
      ["Model safety & alignment research",2,"You engage with it as context, not as a field you track.","Trends reading"],
      ["Mechanistic interpretability",1,"Never discussed. SAEs, activation steering, Anthropic's natural-language autoencoder work — all absent.",""],
      ["Privacy & PII handling in AI systems",2,"Present in your compliance reasoning but never designed for concretely.","Adjacent"],
      ["Supply chain risk (MCP servers, deps)",3,"You flagged MCP servers as a supply-chain surface — and you're one of the few people who authors them, so you know what you're describing.","AMA prep"]
    ]
  },
  {
    d:"Infrastructure, serving & LLMOps",
    note:"Your AWS depth is real and shipped. The LLM-specific ops layer above it is not.",
    t:[
      ["AWS core (IAM, Lambda, ECS/Fargate, SQS)",4,"SpecSync is a real deployed system — multi-environment stacks, queue-driven Fargate services, the whole shape.","SpecSync · celestial newsletter on Lambda"],
      ["Infrastructure as code (CDK)",4,"Python CDK with L3 constructs, parameterised per-environment config, artifact promotion from stage to prod.","SpecSync multi-env stacks"],
      ["CI/CD pipelines",3,"GitHub Actions with OIDC federation, GitLab CI mechanics, immutable git-SHA image tags, manual approval gates.","Celestial · SpecSync"],
      ["Docker & containers",3,"You reasoned your own way to the right answer — the value is dependency consistency and an immutable versioned artifact, not cloud portability — and then built a teaching poster from it.","VM/Docker/K8s poster · Fargate deployments"],
      ["Kubernetes",2,"Correct mental model (orchestration layer above containers, doesn't replace Docker) but deliberately deprioritised and never run.","Poster only, by your own sequencing"],
      ["Local inference (Ollama, LM Studio)",3,"Running locally on the M5, and you debugged a real one — Metal shader / bfloat16 incompatibility, fixed by pinning Ollama 0.18.0.","M5 MacBook, hands-on debugging"],
      ["High-throughput serving (vLLM)",2,"Named as the production-serving tier in your research. Not run.","Research"],
      ["GPU hardware & VRAM economics",3,"VRAM-per-parameter rules, PCIe bottlenecks on dual 3090s, NVLink limits, TOPS comparisons across cards. Well-researched.","Desktop build study"],
      ["Model routing architecture",3,"Your own conclusion from the TCO work, and the right one — route across tiers rather than own hardware.","TRP local inference study"],
      ["Cost management & AI FinOps",3,"You run projects at roughly fifty cents a month and know why. You switched to Haiku for cost reasons deliberately.","Celestial · Hermes work"],
      ["Observability (Splunk, CloudWatch)",3,"Splunk MCP server, a CloudWatch analysis agent, Splunk query design over 24h/30d windows in the triage POC.","Multiple projects"],
      ["API gateway patterns",3,"You mapped AgentCore Gateway onto TRP's existing Apigee layer unprompted — that's the architect move.","AgentCore training"],
      ["LLMOps platforms & model registry",1,"Never discussed. No model versioning, promotion, or registry practice.",""],
      ["Feature stores & ML pipelines",1,"Never discussed.",""],
      ["Edge & on-device inference",2,"Noted that Gemma 4 12B runs in 16GB with vision and voice. Interest, not practice.","Trends reading"]
    ]
  },
  {
    d:"Modalities beyond text",
    note:"Vision is real via the NVIDIA track. Audio and generative media are sketches.",
    t:[
      ["Image classification & vision",3,"MNIST end to end in the browser, plus the VGG16 fruit classifier. The best lesson you drew was about train/serve skew — replicating the preprocessing pipeline exactly.","Digit visualizer · DLI labs"],
      ["NLP & named entity recognition",3,"Covered in the DLI coursework.","NVIDIA DLI NLP/NER labs"],
      ["Speech-to-text",2,"You scaffolded a whisper.cpp pipeline with VAD-gated mic capture. Designed, not run.","voice_twin.py scaffold"],
      ["Text-to-speech & voice cloning",2,"StyleTTS2 / XTTS-v2 chosen, sentence-boundary streaming designed to hide latency. Same status — scaffolded.","voice_twin.py scaffold"],
      ["Vision-language models",2,"Qwen3-VL, Llama 3.2 Vision named in model research.","Research"],
      ["Multimodal architecture",2,"You teach 'vision encoders fused with LLMs' as a line in a table. That's the depth.","Curriculum table"],
      ["Diffusion & image generation",2,"One row in one comparison table. Nothing beyond it.","Passing mention"],
      ["Video generation",1,"Never discussed beyond naming Sora once.",""],
      ["OCR & document AI",2,"Receipt scanning was an agent in the expense concept, but the OCR itself was never the subject.","Adjacent"],
      ["Audio & music generation",1,"Never discussed.",""]
    ]
  },
  {
    d:"Frontier & research directions",
    note:"Almost entirely dark. Defensible for a practitioner — until you're in a room with researchers.",
    t:[
      ["Test-time compute & reasoning scaling",2,"Encountered in trends reading.","Trends"],
      ["World models & JEPA",1,"Never discussed. Over $2B has moved into this thesis in six months.",""],
      ["Physical AI & robotics",2,"Named as where new capital is going. No engagement.","Trends"],
      ["Neuro-symbolic & hybrid AI",2,"Your knowledge-graph-plus-embeddings reasoning is the applied edge of this, though you didn't name it as such.","Implicit"],
      ["Federated learning",1,"Never discussed.",""],
      ["Green AI & energy constraints",2,"You engaged with the power-not-capital argument — interconnection queues, capacity slipping to 2028.","Trends conversation"],
      ["AI economics & compute markets",3,"The TCO study plus the capex/power reading gives you a genuine position on where cost pressure comes from.","TRP study · trends"],
      ["Agentic RL & training environments",1,"Never discussed. This is where a lot of 2026 capability work sits.",""],
      ["Self-improving & recursive systems",1,"Never discussed.",""],
      ["AGI timelines & macro forecasting",2,"Peripheral awareness only.","Trends"]
    ]
  },
  {
    d:"Applied AI & organisational practice",
    note:"Your actual moat. Nobody on your engineering side scores here.",
    t:[
      ["AI adoption strategy",4,"Tools-first sequencing for BAs — Jira/Confluence agents, then Copilot, then the proprietary LLM interface — with measurement of behaviour change rather than licence counts. That's a real strategy.","30-BA programme at TRP"],
      ["AI education & curriculum design",4,"Six-module curriculum, pre-session polling, weekly comics, and the self-awareness to notice the MCP session was too technical and diagnose it as a sequencing and curse-of-knowledge problem.","Delivered, iterated, corrected"],
      ["Use case identification & prioritisation",4,"The regulatory-change-impact and data-lineage agent ideas were good precisely because you know which processes matter — an engineer couldn't have picked them.","Enterprise agent ideation"],
      ["Requirements to architecture translation",4,"This is the BA-to-architect bridge you're actively walking, with steering files and test plans as the mechanism.","POC practice at TRP"],
      ["AI in asset management",4,"ETF NAV/price mechanics, AP arbitrage, EMEA market structure, identifier hierarchy, return metrics. Deep, and it's the context everything else attaches to.","Domain work"],
      ["Change management & measuring adoption",3,"You're pushing toward time studies and adoption metrics as evidence. Not yet produced.","In progress"],
      ["Build vs buy evaluation",3,"You questioned whether to build RAG given managed services, and whether to own hardware given routing. You ask the right question consistently.","Repeated pattern"],
      ["Stakeholder communication & buy-in",3,"You prepare for rooms — the AMA questions were built to be non-dodgeable, and you thought about political dynamics before content.","AMA prep · Nagendra 1:1"],
      ["Explaining AI to non-technical audiences",4,"The restaurant analogy, the dating-trust analogy for the panel, the comic strips. This is a distinct skill and you have it.","Multiple formats, real audiences"],
      ["Portfolio & career positioning",3,"Deliberate about it — projects as evidence, honest about 'shipped agents at scale' being the gap.","Ongoing"]
    ]
  },
  {
    d:"Classical ML, data & engineering craft",
    note:"The pre-LLM half of the field is your thinnest area outside frontier research.",
    t:[
      ["Python",3,"Shipping real code after a fifteen-year gap. Reading and debugging faster than writing from scratch, and honest about that.","Active daily practice"],
      ["Git & version control",3,"Reset, restore, checkout from remote, commit conventions — working fluency.","Daily"],
      ["SQL & data modelling",3,"Career-long BA competence.","Professional background"],
      ["Supervised learning basics",3,"Covered properly through DLI.","NVIDIA DLI"],
      ["Unsupervised learning & clustering",2,"Mentioned as an embedding use case. Never practised.","Adjacent"],
      ["Statistical inference & experiment design",2,"You reason about metrics but haven't designed a controlled experiment. Directly relevant to proving your adoption programme worked.","Gap with immediate business value"],
      ["Time series forecasting",1,"Never discussed — surprising given asset management.",""],
      ["Recommender systems",1,"Never discussed.",""],
      ["Feature engineering",1,"Never discussed.",""],
      ["Data engineering pipelines",2,"SpecSync syncs artifacts rather than moving data at volume. Not the same discipline.","Adjacent"],
      ["Explainable AI (SHAP, LIME)",1,"Never discussed. Relevant to a regulated firm.",""],
      ["Frontend & data visualisation",3,"The digit visualizer, the posters, the interactive frameworks. You build things people can look at.","Multiple artifacts"]
    ]
  }
]