import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./IntroPage.css";

export default function IntroPage() {
  const navigate = useNavigate();
  const [isFadingOut, setIsFadingOut] = useState(false);

  const handleStart = () => {
    setIsFadingOut(true);
    setTimeout(() => {
      navigate("/main"); // chuyển đến giao diện chính
    }, 500); // Đợi hiệu ứng fade-out hoàn tất
  };

  return (
    <div className={`intro-container ${isFadingOut ? "fade-out" : ""}`}>
      <div className="intro-content">
        <img
          src="/images/avatar.jpg"
          alt="Avatar"
          className="intro-avatar"
        />
        <h1 className="intro-title">
          Chào mừng bạn đến với hệ thống dự đoán giá trị bất động sản
        </h1>
        <p className="intro-desc">
          Website sử dụng AI để ước lượng giá bất động sản một cách chính xác, giúp bạn ra quyết định đầu tư hiệu quả.
        </p>
        <p className="intro-note">
          Dự án được phát triển bởi cá nhân tôi – nhấn mạnh tính minh bạch và công nghệ tiên tiến.
        </p>
        <button onClick={handleStart} className="intro-button">
          Bắt đầu trải nghiệm
        </button>
      </div>
    </div>
  );
}
