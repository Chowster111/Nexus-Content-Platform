# Engineering Blog Recommender – Frontend

This is the **React + TypeScript** frontend for the **Engineering Blog Recommender**, a modern AI-powered system for discovering, searching, and recommending high-quality engineering articles from sources like Netflix, Airbnb, Uber, Stripe, and more.

---

## Key Features

* **Search & Recommendations:** Perform semantic keyword searches or get personalized article suggestions based on user likes.
* **Swipe Mode:** Tinder-like swipe-to-like/dislike interaction for quick curation.
* **User Auth:** Sign up, sign in, and persist likes per user with Supabase Auth.
* **Analytics Dashboard:** Displays top sources and categories, dynamically fetched from the backend.
* **Observability Ready:** Integrated Sentry for frontend error tracking and retry logic on API calls.
* **Responsive UI:** Fully responsive, modern layout built with Vite, React, and TypeScript.
* **Smooth Animations:** Framer Motion for subtle transitions and swipe gestures.
* **Three.js Background:** Animated wireframe scene for a sleek developer feel.

---

## Tech Stack

| Tool/Library               | Purpose                                               |
| -------------------------- | ----------------------------------------------------- |
| **React + TypeScript**     | Strongly typed UI with reusable components            |
| **Vite**                   | Lightning-fast frontend build tool                    |
| **Supabase Auth**          | User authentication and session management            |
| **Axios**                  | HTTP client for calling FastAPI backend endpoints     |
| **Framer Motion**          | Animations and swipe gestures                         |
| **Sentry**                 | Client-side error tracking and performance monitoring |
| **Three.js**               | Dynamic animated background scene                     |
| **CSS Modules**            | Scoped styling                                        |
| **React-Loading-Skeleton** | Async loading placeholders                            |

---

## Project Structure

```
frontend/
├── public/                # Static assets
├── src/
│   ├── components/        # UI components (Header, ToggleSwitch, Results, SwipeResults, AnalyticsBox)
│   ├── pages/             # Pages (Home.tsx, more pages in the future)
│   ├── services/          # API clients and likes handler
│   ├── styles/            # CSS Modules
│   ├── App.tsx            # App entry point
│   ├── main.tsx           # Vite entry script
│   ├── lib/               # Supabase client setup
├── vite.config.ts         # Vite config
└── index.html
```

---

## Authentication

* Auth is handled using Supabase Auth.
* On sign in / sign up, a session is stored and used to link likes to the current user.
* Likes are saved via `likesClient.ts` with retry and Sentry error capture.

---

## Analytics

* The homepage includes a **Site Analytics** section showing top sources and categories.
* Analytics data is fetched via FastAPI endpoints and rendered in a clean, responsive table.
* Server-side responses are cached with proper `Cache-Control` headers for performance.

---

## How to Run Locally

1. **Install Dependencies**

   ```bash
   cd frontend
   npm install
   ```

2. **Set Environment Variables**

   Create `.env` for your Supabase keys:

   ```
   VITE_SUPABASE_URL=your-supabase-url
   VITE_SUPABASE_ANON_KEY=your-supabase-anon-key
   VITE_SENTRY_DSN=your-sentry-dsn
   ```

3. **Start the Dev Server**

   ```bash
   npm run dev
   ```

   The frontend will run on `http://localhost:3000` by default.

---

## Deployment Notes

* The frontend is **CORS-enabled** and expects the FastAPI backend to run on `/api` (reverse-proxied if needed).
* Built assets can be served via any static host (e.g., Vercel, Netlify, or as part of a container).
* Configure your production Sentry DSN to capture real frontend issues in production.

---

## Example API Flow

* `/api/search/articles` → Semantic keyword search.
* `/api/find/recommend` → Personalized article recommendations.
* `/api/user/likes` → Save or update user likes.
* `/api/analytics/*` → Site usage stats for the analytics dashboard.

---

## Best Practices Included

* Retry logic with exponential backoff for critical API calls.
* Error boundaries and Sentry capture for unhandled errors.
* Auth-aware UI for toggling state when logged in vs. anonymous.
* Flexible `ToggleSwitch` to switch between search and recommendations.

---

## Author

Arijit Chow