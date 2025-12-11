import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    
    // Forward the request to FastAPI backend
    const response = await fetch(`${BACKEND_URL}/generate`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      return NextResponse.json(error, { status: response.status });
    }

    // Return the image blob
    const blob = await response.blob();
    return new NextResponse(blob, {
      headers: {
        "Content-Type": "image/png",
      },
    });
  } catch (error) {
    console.error("Render error:", error);
    return NextResponse.json(
      { error: "Failed to connect to rendering service" },
      { status: 500 }
    );
  }
}