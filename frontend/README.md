# Space Reimagined - Frontend

Upload a floorplan or room photo and see it transformed into any interior style using AI.

## Features

- Upload any floorplan or room image
- Choose from 8 interior styles (Scandinavian, Mid-Century Modern, Industrial, etc.)
- Get photorealistic renders powered by Google Gemini
- Side-by-side before/after comparison
- Download rendered images

## Tech Stack

- Next.js 14 (App Router)
- TypeScript
- Ant Design
- CSS Modules

## Getting Started

### Prerequisites

- Node.js 18+
- Backend server running (see `/backend` folder)

### Installation
```bash
npm install
```

### Environment Variables

Create a `.env.local` file:
```
BACKEND_URL=http://localhost:8000
```

### Run Development Server
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see the app.

## Project Structure
```
frontend/
├── app/
│   ├── api/render/      # API route (proxies to backend)
│   ├── page.tsx         # Main page component
│   ├── page.module.css  # Styles
│   └── layout.tsx       # Root layout
├── public/
│   ├── blueprint-before.png  # Example images
│   └── blueprint-after.png
└── package.json
```

## Deployment

Deployed on [Vercel](https://vercel.com). Set `BACKEND_URL` environment variable to your production backend URL.