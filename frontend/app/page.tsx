"use client";

import React, { useState } from "react";
import { Card, Upload, Button, Select, message } from "antd";
import { UploadOutlined, DeleteOutlined, DownloadOutlined } from "@ant-design/icons";
import styles from "./page.module.css";

const STYLE_OPTIONS = [
  { value: "1", label: "Scandinavian Modern" },
  { value: "2", label: "Mid-Century Modern" },
  { value: "3", label: "Industrial Loft" },
  { value: "4", label: "Minimalist Japanese" },
  { value: "5", label: "Contemporary Luxury" },
  { value: "6", label: "Coastal / Hamptons" },
  { value: "7", label: "Art Deco" },
  { value: "8", label: "Rustic Farmhouse" },
];

export default function HomePage() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [renderUrl, setRenderUrl] = useState<string | null>(null);
  const [styleNumber, setStyleNumber] = useState<string>("1");
  const [loading, setLoading] = useState(false);

  const handleUpload = (info: any) => {
    const uploaded = info.file.originFileObj || info.file;
    setFile(uploaded);
    
    if (uploaded) {
      const url = URL.createObjectURL(uploaded);
      setPreviewUrl(url);
    }
    
    if (renderUrl) {
      URL.revokeObjectURL(renderUrl);
      setRenderUrl(null);
    }
  };

  const handleRemove = () => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    if (renderUrl) {
      URL.revokeObjectURL(renderUrl);
    }
    setFile(null);
    setPreviewUrl(null);
    setRenderUrl(null);
  };

  const handleDownload = () => {
    if (!renderUrl) return;
    
    const a = document.createElement("a");
    a.href = renderUrl;
    a.download = "render.png";
    a.click();
  };

  const handleStartOver = () => {
    handleRemove();
  };

  const handleSubmit = async () => {
    if (!file) {
      message.error("You must upload a blueprint first.");
      return;
    }

    setLoading(true);
    
    if (renderUrl) {
      URL.revokeObjectURL(renderUrl);
      setRenderUrl(null);
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("style_number", styleNumber);

    try {
      const res = await fetch("/api/render", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        message.error("Render failed.");
        return;
      }

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      setRenderUrl(url);
      message.success("Render complete!");
    } catch (error) {
      message.error("An error occurred during rendering.");
    } finally {
      setLoading(false);
    }
  };

  const cardClassName = renderUrl 
    ? `${styles.card} ${styles.cardExpanded}` 
    : styles.card;

  // Show results view after render is complete
  if (renderUrl && previewUrl) {
    return (
      <div className={styles.container}>
        <Card className={cardClassName}>
          <div className={styles.title}>Floorplan Renderer</div>
          <div className={styles.subtitle}>
            Your rendered floorplan is ready.
          </div>

          <div className={styles.resultsHeader}>
            <span className={styles.resultsTitle}>Result</span>
            <div className={styles.resultsActions}>
              <Button onClick={handleStartOver}>
                Start Over
              </Button>
              <Button type="primary" icon={<DownloadOutlined />} onClick={handleDownload}>
                Download Render
              </Button>
            </div>
          </div>
          
          <div className={styles.comparisonGrid}>
            <div>
              <div className={styles.comparisonLabel}>Blueprint</div>
              <div className={styles.comparisonImageFrame}>
                <img
                  src={previewUrl}
                  alt="Blueprint"
                  className={styles.comparisonImage}
                />
              </div>
            </div>
            
            <div>
              <div className={styles.comparisonLabel}>Rendered</div>
              <div className={styles.comparisonImageFrame}>
                <img
                  src={renderUrl}
                  alt="Rendered result"
                  className={styles.comparisonImage}
                />
              </div>
            </div>
          </div>
        </Card>
      </div>
    );
  }

  // Show upload view before render
  return (
    <div className={styles.container}>
      <Card className={styles.card}>
        <div className={styles.title}>Floorplan Renderer</div>
        <div className={styles.subtitle}>
          Upload a blueprint and choose an interior style.
        </div>

        <label className={styles.label}>Blueprint Image</label>
        
        {previewUrl ? (
          <div className={styles.previewContainer}>
            <div className={styles.imageFrame}>
              <img
                src={previewUrl}
                alt="Blueprint preview"
                className={styles.previewImage}
              />
            </div>
            <Button
              icon={<DeleteOutlined />}
              danger
              onClick={handleRemove}
              size="small"
            >
              Remove
            </Button>
          </div>
        ) : (
          <Upload
            beforeUpload={() => false}
            onChange={handleUpload}
            maxCount={1}
            showUploadList={false}
            accept="image/*"
          >
            <Button icon={<UploadOutlined />}>Choose Blueprint</Button>
          </Upload>
        )}

        <div className={styles.spacerSmall} />

        <label className={styles.label}>Interior Style</label>
        <Select
          value={styleNumber}
          onChange={setStyleNumber}
          options={STYLE_OPTIONS}
          style={{ width: "100%" }}
        />

        <div className={styles.spacerLarge} />

        <Button type="primary" block onClick={handleSubmit} loading={loading}>
          {loading ? "Rendering..." : "Render Blueprint"}
        </Button>
      </Card>
    </div>
  );
}