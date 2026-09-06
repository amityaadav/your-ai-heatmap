# Requirements: AI Knowledge Quiz & Heatmap Generator

## Goal
Transform the static AI Knowledge Heatmap into a dynamic system that assesses a user's AI/ML knowledge through a quiz and generates a personalized heatmap based on the results.

## Functional Requirements
1. **Topic Catalog**: The system must use the same 148 topics across 12 domains defined in the original heatmap. ✅
2. **Quiz Engine**:
   - Present topics one by one in domain order. ✅
   - Open-ended explanation fields where users describe their knowledge. ✅
   - LLM-evaluated scoring (not self-reported). ✅
3. **Scoring Logic**:
   - LLM evaluates the depth of an answer to assign a level (1-4). ✅
   - Cross-topic credit: if the user's answer demonstrates knowledge of other pending topics, those get auto-scored and struck from the queue. ✅
   - Scoring rubric: L1 (Untouched), L2 (Heard of it), L3 (Can explain to peers), L4 (Can teach / have built). ✅
4. **Heatmap Generation**:
   - Generate a visual heatmap (matching the original design) based on the session's scores. ✅
   - Download as `index_final.html`. ✅
5. **Persistence**:
   - LocalStorage save/resume for long quizzes. ✅
6. **Rate Limiting**:
   - IP-based: 200 requests/day, 1000 requests/hour to prevent abuse. ✅

## Non-Functional Requirements
- **Preservation**: The original `index.html` must remain untouched as the design gold standard. ✅
- **Performance**: Single-page application (SPA) feel; fast transitions between quiz questions. ✅
- **UX/UI**: Maintain the high-contrast, technical aesthetic (Space Grotesk, IBM Plex) from the mockup. ✅
- **Backend**: FastAPI + Ollama for LLM-powered evaluation. ✅

## Architecture
- **Backend**: `backend/main.py` (FastAPI), `backend/sensing_engine.py` (LLM evaluator), `backend/models.py` (Pydantic schemas)
- **Frontend**: `quiz.html` (single-file SPA, no build step)
- **Data**: `assets/js/data.js` (148 topics), `assets/data/amit-profile.json` (canonical scored profile with learning resources)
