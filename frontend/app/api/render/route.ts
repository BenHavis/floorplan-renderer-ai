import { NextRequest, NextResponse } from "next/server";

// Always use your deployed backend URL
const BACKEND_URL = "https://floorplan-renderer-ai-production.up.railway.app";

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();

    // Forward blueprint + style to FastAPI backend
    const response = await fetch(`${BACKEND_URL}/generate`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: "Unknown error" }));
      return NextResponse.json(error, { status: response.status });
    }

    // Return image back to browser
    const blob = await response.blob();

    return new NextResponse(blob, {
      headers: { "Content-Type": "image/png" },
    });

  } catch (error) {
    console.error("Render error:", error);
    return NextResponse.json(
      { error: "Failed to reach backend service" },
      { status: 500 }
    );
  }
}
