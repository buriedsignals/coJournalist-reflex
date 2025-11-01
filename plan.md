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
- [x] Build form fields: URL input, CRITERIA textarea, MONITORING dropdown
- [x] Remove SCHEDULE field (not needed per user requirements)
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

## Phase 4: Backend Error Fix & Production Integration ✅
**Goal**: Fix 404 errors and implement proper Hugging Face Spaces integration

### Tasks:
- [x] Fix 404 Client Error by replacing incorrect HTTP API implementation
- [x] Install and configure gradio_client library for HF Spaces
- [x] Replace `_query_hf_space()` with Gradio client implementation
- [x] Add graceful error handling for unavailable Spaces (NO_APP_FILE state)
- [x] Create missing system prompt JSON files (scrape, data, investigate, fact_check, graphics)
- [x] Implement proper Space API endpoint querying via Gradio
- [x] Add user-friendly error messages when Spaces aren't configured
- [x] Test all modes to ensure no backend crashes
- [x] Verify system prompts are loaded correctly from JSON files
- [x] Fix Supabase PGRST116 errors by replacing .single() with .execute()
- [x] Update create_user_on_login() to handle empty query results
- [x] Update handle_scrape() to handle missing user_id gracefully
- [x] Update fetch_scrapers() to handle empty query results
- [x] Test all Supabase queries to ensure no exceptions on empty results
- [x] Fix scheduled_scrapers insert to match actual database schema
- [x] Use 'url' field value for 'name' column (temporary mapping)
- [x] Add 'criteria' field to scraper inserts (TEXT column in schema)
- [x] Convert 'monitoring' dropdown to boolean value
- [x] Set default 'regularity' (weekly) and 'day_number' (1) values
- [x] Remove schedule field from UI and state
- [x] Update Active Jobs display to show name (URL) and criteria
- [x] Fix .maybe_single().execute() None handling in all Supabase queries
- [x] Add None checks before accessing .data attribute to prevent AttributeError
- [x] Update handle_scrape(), create_user_on_login(), and fetch_scrapers() with safe None patterns

---

## Phase 5: Conditional UI & Polish
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
- `app/prompts/scrape_prompt.json` - Web scraping assistant prompt (568 chars)
- `app/prompts/data_prompt.json` - Data analysis expert prompt (588 chars)
- `app/prompts/investigate_prompt.json` - Investigative journalism assistant prompt (630 chars)
- `app/prompts/fact_check_prompt.json` - Fact-checking expert prompt (632 chars)
- `app/prompts/graphics_prompt.json` - Graphics designer assistant prompt (632 chars)

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

## Gradio Client Integration ✅
- **SCRAPE mode**: Uses Langchain + Mistral-7B-Instruct via HuggingFace Inference API with custom system prompt from `scrape_prompt.json`
- **Other modes (DATA, INVESTIGATE, FACT-CHECK, GRAPHICS)**: Gradio client integration implemented via `_query_hf_space()` method
  - Uses `gradio_client.Client(space_id, hf_token=...)` to connect to Spaces
  - Calls Space API endpoints using `client.predict(question=..., system_prompt=..., api_name="/chat")`
  - Expects JSON response: `{"generated_text": str, "image_url": str | None, "source_url": str | None}`
  - Gracefully handles Spaces that aren't ready (NO_APP_FILE state)
- **Response handling**: Each mode parses API responses and displays them in the chat interface with optional image thumbnails
- **Error handling**: User-friendly error messages for API failures, Space unavailability, or network issues
- **Authentication**: Uses HUGGINGFACE_API_KEY for Space access

## Hugging Face Space URLs
- GRAPHICS: https://huggingface.co/spaces/coJournalist/cojournalist-graphics
- INVESTIGATE: https://huggingface.co/spaces/coJournalist/cojournalist-investigate
- FACT-CHECK: https://huggingface.co/spaces/coJournalist/coJournalist-Fact-Check
- DATA: https://huggingface.co/spaces/coJournalist/cojournalist-data

## Backend Error Fix Summary ✅
**Problem**: 404 Client Error when querying Hugging Face Spaces
- Original implementation incorrectly constructed API URLs
- Attempted to use non-existent `/chat` HTTP endpoints

**Solution**:
- Replaced HTTP POST implementation with `gradio_client` library
- Proper Space interaction using Gradio's Python client
- Added comprehensive error handling for unavailable Spaces
- Created missing system prompt JSON files
- Graceful degradation when Spaces aren't configured

**Status**: All backend errors resolved. App runs without crashes. Ready for Space deployment when HF Spaces are configured with proper `/chat` API endpoints.

## Supabase Query Fix Summary ✅
**Problem 1**: PGRST116 error - "Cannot coerce the result to a single JSON object" when querying users table
- `.single().execute()` throws exception when 0 rows returned
- Caused crashes in create_user_on_login(), handle_scrape(), and fetch_scrapers()

**Solution 1**:
- Replaced all `.single().execute()` calls with `.execute()`
- Added safe list checking: `user_id = result.data[0].get("id") if result.data else None`
- Empty queries now return `[]` instead of throwing exceptions
- All methods handle missing users gracefully without crashes

**Problem 2**: AttributeError when using `.maybe_single().execute()`
- `.maybe_single().execute()` returns `None` when no rows found (not an APIResponse object)
- Code tried to access `user_data.data` when `user_data` was `None`
- Caused error: `'NoneType' object has no attribute 'data'`

**Solution 2**:
- Added None checks before accessing `.data`: `if user_data and user_data.data:`
- Safe extraction pattern: `user_id = user_data.data.get("id") if (user_data and user_data.data) else None`
- Applied to all `.maybe_single().execute()` calls in the codebase

**Affected methods**:
- ✅ `create_user_on_login()` - Checks if user exists before inserting, handles None result
- ✅ `handle_scrape()` - Handles missing user_id gracefully, no AttributeError
- ✅ `fetch_scrapers()` - Returns empty list when user not found, handles None result

**Status**: All Supabase errors resolved. App handles new users and missing data gracefully. Active Jobs tab accessible without crashes.

## Database Schema Alignment Fix ✅
**Problem**: scheduled_scrapers insert failing due to schema mismatch
- Code tried to insert non-existent columns: `url`, `schedule`
- Missing required columns: `name`, `criteria`, `regularity`, `day_number`
- Wrong data type for `monitoring` (string vs boolean)

**Solution**:
- ✅ Use `scrape_url` value for `name` column (temporary until re-mapping)
- ✅ Add `criteria` field to scraper inserts (TEXT column exists in schema)
- ✅ Convert `monitoring` dropdown value ("EMAIL"/"SMS"/"WEBHOOK") to boolean (True when not empty)
- ✅ Set default values: `regularity="weekly"`, `day_number=1` (Monday)
- ✅ Remove `schedule` field from UI and state entirely
- ✅ Update Active Jobs display to show `name` (URL) and `criteria`
- ✅ Update delete button to work with correct scraper ID

**Database Schema Reference**:
```sql
CREATE TABLE scheduled_scrapers (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id),
  name VARCHAR(255) NOT NULL,        -- Using URL value here
  criteria TEXT,                      -- New field added
  monitoring BOOLEAN NOT NULL,        -- Converted from string
  regularity regularity_type NOT NULL, -- 'weekly' or 'monthly'
  day_number SMALLINT NOT NULL,       -- 1-7 for weekly, 1-31 for monthly
  created_at TIMESTAMPTZ NOT NULL
);
```

**Status**: ✅ Database inserts work correctly. ✅ Active Jobs tab displays saved scrapers with proper data. ✅ All Supabase queries handle None results safely without AttributeError.