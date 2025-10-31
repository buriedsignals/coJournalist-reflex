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

## Hugging Face Space URLs
- GRAPHICS: https://huggingface.co/spaces/coJournalist/cojournalist-graphics
- INVESTIGATE: https://huggingface.co/spaces/coJournalist/cojournalist-investigate
- FACT-CHECK: https://huggingface.co/spaces/coJournalist/coJournalist-Fact-Check
- DATA: https://huggingface.co/spaces/coJournalist/cojournalist-data
