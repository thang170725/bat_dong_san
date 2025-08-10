import React from 'react'; // Cần import React để sử dụng JSX (ví dụ: <App />)
import ReactDOM from 'react-dom/client'; // Cần import ReactDOM để tương tác với DOM
import App from './App'; // **ĐÚNG:** Import component App của bạn. Đảm bảo App.js có 'export default App;'
import './index.css'; // Import file CSS tổng thể (nếu có)
import { BrowserRouter } from 'react-router-dom';
import AppRouter from './AppRouter'; // tạo file này để quản lý route

// Tìm thẻ HTML có id='root' trong file public/index.html của bạn
// Đây là nơi ứng dụng React của bạn sẽ được "gắn" vào
const root = ReactDOM.createRoot(document.getElementById('root'));

// Render (hiển thị) component App của bạn vào DOM
// // <React.StrictMode> là tùy chọn, giúp phát hiện các vấn đề tiềm ẩn trong quá trình phát triển
// root.render(
//   <React.StrictMode>
//     <App /> {/* **ĐÚNG:** Sử dụng component App đã import như một JSX element */}
//   </React.StrictMode>
// );
root.render(
  <BrowserRouter>
    <AppRouter />
  </BrowserRouter>
);