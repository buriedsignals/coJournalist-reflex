# coJournalist - AI-Powered Journalism Assistant

## Project Overview
A web application with Clerk authentication that uses Langchain and Hugging Face to route user chat requests to 5 different modes:
- **SCRAPE**: Direct Python implementation for web scraping with scheduling and monitoring (N8N webhook integration)
- **DATA**: Routes to Hugging Face Space for data analysis
- **INVESTIGATE**: Routes to Hugging Face Space for investigative research
- **FACT-CHECK**: Routes to Hugging Face Space for fact verification
- **GRAPHICS**: Routes to Hugging Face Space for graphic generation

User manually selects mode via UI buttons - no AI routing.

---

## Phase 1: Authentication & Base UI ✅
**Goal**: Set up Clerk authentication and create the main interface layout with mode selection

### Tasks:
- [x] Configure Clerk authentication with publishable and secret keys
- [x] Create protected main chat interface with header (Profile/Sign Out buttons)
- [x] Implement coJournalist branding with logo styling
- [x] Build mode selection buttons (SCRAPE, DATA, INVESTIGATE, FACT-CHECK, GRAPHICS)
- [x] Add active state styling for selected mode
- [x] Create chat input field with send button icon
- [x] Implement basic routing between authenticated and unauthenticated states

---

## Phase 2: SCRAPE Mode UI & Logic ✅
**Goal**: Build the SCRAPE mode with sidebar form and Python-based scraping functionality

### Tasks:
- [x] Create left sidebar that appears when SCRAPE mode is active
- [x] Build form fields: URL input, SCHEDULE input, CRITERIA textarea, MONITORING dropdown
- [x] Implement state management for scrape configuration
- [x] Add Python scraping logic using requests/BeautifulSoup
- [x] Create event handler to process scraping requests
- [x] Display scraping results in chat interface with card layout
- [x] Add error handling and loading states for scraping operations

---

## Phase 3: Hugging Face Integration & Mode Routing ✅
**Goal**: Integrate Langchain with Hugging Face Inference API and route requests to appropriate modes

### Tasks:
- [x] Install and configure langchain and huggingface_hub libraries
- [x] Set up Hugging Face Inference API client with API key
- [x] Create routing logic to classify user intent and select appropriate mode
- [x] Implement handlers for DATA, INVESTIGATE, FACT-CHECK, and GRAPHICS modes
- [x] Connect each mode to Hugging Face Space endpoint (dummy placeholder)
- [x] Build chat message display with user/assistant distinction
- [x] Add response streaming or loading indicators
- [x] Handle errors and API rate limits gracefully
- [x] Configure dev mode authentication for test@cojournalist.com
- [x] Implement conditional UI (sidebar only in SCRAPE mode)
- [x] Disable chat in SCRAPE mode until scrape results returned
- [x] Switch from AI routing to user-selected mode routing
- [x] Configure Hugging Face Space URLs for each mode
- [x] Add "Open Space" button for non-SCRAPE modes
- [x] Integrate N8N webhook for SCRAPE mode (https://n8n-cojournalist.onrender.com/webhook/lipsum)
- [x] Create per-mode system prompt JSON files (5 files in app/prompts/)
- [x] Implement separate chat histories per mode (persists within mode, clears on switch)
- [x] Prepare HTTP API integration structure for querying HF Spaces

---

## Phase 4: Conditional UI & Polish
**Goal**: Add mode-specific UI elements and refine the overall user experience

### Tasks:
- [ ] Implement conditional rendering based on selected mode
- [ ] Add mode-specific UI elements (e.g., data visualizations, fact-check badges)
- [ ] Create About section/modal with app information
- [ ] Polish responsive design for mobile and desktop
- [ ] Add transitions and animations for mode switching
- [ ] Implement chat history persistence per session
- [ ] Add user profile page integration with Clerk
- [ ] Final testing of all modes and authentication flows

---

## Notes
- Clerk keys: CLERK_PUBLISHABLE_KEY, CLERK_SECRET_KEY (already available)
- Hugging Face key: HUGGINGFACE_API_KEY (already available)
- Dev mode enabled for test@cojournalist.com (no email verification required)
- **User-selected mode routing**: Users click mode buttons to switch between modes (no AI routing)
- **Hugging Face Spaces**: Each mode (except SCRAPE) has an "Open Space" button that opens the HF Space in a new tab
- **N8N Webhook**: SCRAPE mode sends JSON payload to https://n8n-cojournalist.onrender.com/webhook/lipsum
- SCRAPE mode: Chat disabled until scrape results returned, then enabled for confirmation
- Conditional UI: Sidebar only shows in SCRAPE mode, all other modes show chat only
- Each mode should have distinct visual feedback when active
- Chat interface supports scrolling with message history

## System Prompts ✅
Each mode has a customizable system prompt stored in JSON files:
- `app/prompts/scrape_prompt.json` - Web scraping assistant prompt (627 chars)
- `app/prompts/data_prompt.json` - Data analysis expert prompt (662 chars)
- `app/prompts/investigate_prompt.json` - Investigative journalism assistant prompt (707 chars)
- `app/prompts/fact_check_prompt.json` - Fact-checking expert prompt (732 chars)
- `app/prompts/graphics_prompt.json` - Graphics designer assistant prompt (730 chars)

**These files are editable - you can modify them to customize AI behavior for each mode.**

JSON structure:
```json
{
  "prompt": "Your system prompt text here..."
}
```

## Chat History Behavior ✅
- **Separate histories per mode**: Each mode maintains its own conversation thread via `chat_histories: dict[Mode, list[Message]]`
- **History persistence**: Chat history persists within a mode during the session
- **No cross-mode persistence**: Switching modes shows that mode's history (does not carry over)
- **Session-only**: History is not saved beyond the current session
- **Welcome messages**: When switching to a new mode (except SCRAPE), a welcome message appears

## HTTP API Integration ✅
- **SCRAPE mode**: Uses Langchain + Mistral-7B-Instruct via HuggingFace Inference API with custom system prompt from `scrape_prompt.json`
- **Other modes (DATA, INVESTIGATE, FACT-CHECK, GRAPHICS)**: HTTP POST integration implemented via `_query_hf_space()` method
  - Constructs API URL from HF Space URL (converts `/spaces/` to `/spaces/api/` and appends `/chat`)
  - Sends POST request with `Authorization: Bearer {HUGGINGFACE_API_KEY}` header
  - Payload includes: `{"inputs": question, "parameters": {"system_prompt": system_prompt}}`
  - Expects JSON response: `{"generated_text": str, "image_url": str | None, "source_url": str | None}`
- **Response handling**: Each mode parses API responses and displays them in the chat interface with optional image thumbnails
- **Error handling**: Graceful error messages for API failures, timeouts, or network issues
- **Timeout**: 30 seconds for HF Space API requests

## Hugging Face Space URLs
- GRAPHICS: https://huggingface.co/spaces/coJournalist/cojournalist-graphics
- INVESTIGATE: https://huggingface.co/spaces/coJournalist/cojournalist-investigate
- FACT-CHECK: https://huggingface.co/spaces/coJournalist/coJournalist-Fact-Check
- DATA: https://huggingface.co/spaces/coJournalist/cojournalist-data

## Implementation Details

### Per-Mode System Prompts
- Prompts loaded from JSON files at runtime in `process_chat()` event handler
- Each mode reads its prompt before processing chat requests
- Filename pattern: `{mode_name}_prompt.json` (hyphens converted to underscores)
- Example: `FACT-CHECK` → `fact_check_prompt.json`
- Used to guide AI behavior for each journalism task
- Prompts are comprehensive (600-730 characters) and describe role, capabilities, and interaction guidelines

### Separate Chat Histories
- State uses `chat_histories: dict[Mode, list[Message]]` to store per-mode conversations
- Computed var `chat_history` returns current mode's history
- Mode switching triggers welcome message for non-SCRAPE modes
- Each mode's conversation persists independently during the session
- Verified working: switching between modes maintains separate conversation threads

### HTTP API Integration (Production-Ready)
- `_query_hf_space()` method handles API calls to Hugging Face Spaces
- Constructs proper API endpoint URLs from Space URLs
- Includes authorization headers with HUGGINGFACE_API_KEY
- Sends POST requests with user question and system prompt
- Expects JSON response with `generated_text`, optional `image_url`, and `source_url`
- Displays responses in chat with optional image thumbnails
- Full error handling with try/except for network errors
- 30-second timeout to prevent hanging requests

### Current Status
All core features implemented and tested:
- ✅ Per-mode system prompts (5 JSON files created)
- ✅ Separate chat histories per mode
- ✅ HTTP API integration ready for HF Spaces
- ✅ N8N webhook integration for SCRAPE mode
- ✅ Conditional UI based on active mode
- ✅ Authentication with Clerk
- ✅ Mode switching with active state styling

**Ready for testing!** You can now:
1. Edit JSON files in `app/prompts/` to customize AI behavior
2. Switch between modes to see separate conversation threads
3. Send questions that will query Hugging Face Space APIs (when Spaces are ready)
