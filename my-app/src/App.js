import React, {useState} from 'react';
import './App.css'; // Assuming you'll put the CSS in App.css

function Header() {
  return (
    <header className="app-header">
      <div className="logo">
        <span className="letter-logo1">T</span>
        <span className="letter-logo2">com.AI</span>
        {/* <div className="background-logo background-logo1"></div>
        <div className="background-logo background-logo2"></div> */}
      </div>

      <nav className="auth-links">
        <div className="login">Login</div>
        <div className="logup">Logup</div>
      </nav>
    </header>
  );
}

function MainTitle() {
  return (
    <div className="main-title-section">
      <h1 className="main-heading">DỰ ĐOÁN GIÁ BẤT ĐỘNG SẢN BẰNG AI</h1>
      <p className="sub-heading">GIAO DIỆN PHẾ NHƯNG KẾT QUẢ KHÔNG PHẾ !!</p>
    </div>
  );
}

function SidebarNavigation({onSelectOption}) {
  return (
    <div className="sidebar">
      <div className="option" onClick={()=>onSelectOption("dia-diem")}>
        Địa Điểm
      </div>
      <div className="option" onClick={()=>onSelectOption("so-phong-ngu")}>
        Số phòng ngủ
      </div>
      <div className="option" onClick={()=>onSelectOption("dien-tich")}>
        Diện Tích
      </div>
      <div className="option" onClick={()=>onSelectOption("loai-nha")}>
        Loại Nhà
      </div>
      <div className="option" onClick={()=>onSelectOption("giay-to-phap-ly")}>
        Giấy tờ Pháp Lý
      </div>
      <div className="option" onClick={()=>onSelectOption("vi-tri")}>
        Vị Trí
      </div>
      <div className="option" onClick={()=>onSelectOption("mat-tien")}>
        Mặt Tiền
      </div>
      <div className="option" onClick={()=>onSelectOption("tinh-trang-nha")}>
        Tình Trạng Nhà
      </div>
      <div className="option" onClick={()=>onSelectOption("tang")}>
        Tầng
      </div>
      <div className="option" onClick={()=>onSelectOption("mo-ta")}>
        Mô Tả
      </div>     
    </div>
  );
}

function toSnakeCaseVN(str) {
  str = String(str);
  return str.normalize("NFD")                         // tách dấu
            .replace(/[\u0300-\u036f]/g, "")          // bỏ dấu
            .replace(/đ/g, "d").replace(/Đ/g, "D")    // đ → d
            .toLowerCase()
            .trim()
            .replace(/\s+/g, "_");                    // khoảng trắng → gạch dưới
}

function SupportContent({selected, updateData, setNote}){
  if (!selected) {
    return (
      <div className="box-option">
        <div className="list-option">
          <p>Chọn một tuỳ chọn ở bên trái để nhập dữ liệu.</p>
        </div>
      </div>
    );
  }

  if (selected === "dia-diem"){
    const list = [
      "Ba Đình",
      "Bắc Từ Liêm",
      "Cầu Giấy",
      "Đống Đa",
      "Hà Đông",
      "Hai Bà Trưng",
      "Hoàn Kiếm",
      "Hoàng Mai",
      "Long Biên",
      "Nam Từ Liêm",
      "Thanh Xuân",
      "Ba Vì",
      "Chương Mỹ",
      "Đan Phượng",
      "Đông Anh",
      "Gia Lâm",
      "Hoài Đức",
      "Mê Linh",
      "Mỹ Đức",
      "Phú Xuyên",
      "PHúc Thọ",
      "Quốc Oai",
      "Sóc Sơn",
      "Thạch Thất",
      "Thanh Oai",
      "Thanh Trì",
      "Thường Tín",
      "Ứng Hòa",
      "Sơn Tây"
    ];

    return (
      <div className="box-option">
        <div className="list-option">
          {list.map((label, i) => (
            <div key={i} onClick={() => updateData("dia_diem", {
              label: label,
              value: toSnakeCaseVN(label)
            })}>
              {label}
            </div>
          ))}          
        </div>
      </div>
    );
  }
  
  if (selected === "so-phong-ngu") {
    const list = [
      1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20
    ]
    return (
      <div className="box-option">
        <div className="list-option">
          {list.map((label, i) => (
            <div key={i} onClick={() => updateData("so_phong_ngu", {
              label: label,
              value: toSnakeCaseVN(label)
            })}>
              {label}
            </div>
          ))}
        </div>      
      </div>
    );
  }

  if (selected === "dien-tich") {
    return (
      <div className="box-option">
        <div className="list-option">
          <input 
            type="number" 
            placeholder="Đơn vị m2"
            onChange={(e) => updateData("dien_tich", {
              label: e.target.value,
              value: e.target.value
            })}
          />
        </div>      
      </div>
    );
  }

  if (selected === "loai-nha") {
    const list = [
      "Biệt thự", 
      "Căn hộ cao cấp", 
      "Căn hộ", 
      "Quỹ căn hộ", 
      "Nhà đất"
    ]

    return (
      <div className="box-option">
        <div className="list-option">
          {list.map((label, i) => {
            const value = toSnakeCaseVN(label);
            return (
              <div 
                key={i} 
                onClick={() => {
                  updateData("loai_nha", {label: label, value});

                  let note = ""

                  if (label === "Biệt thự") {
                    note =
                      " - Biệt thự là nhà có diện tích >=250, số tầng <= 3 và các điều kiện phù hợp khác\n" + 
                      " - Lưu ý: Nếu cố tình cài đặt sai kích thước thì mô hình sẽ không thể cho ra kết quả đúng\n" +
                      "Ví dụ: Biệt thự - 300 m2 - 5-6 phòng ngủ (Đúng), Biệt thự - 300 m2 - 1-2 phòng ngủ (Sai)"
                  }

                  if (label === "Căn hộ cao cấp" || 
                    label === "Căn hộ" ||
                    label === "Quỹ căn hộ") {
                      updateData("tang", {label: "1", value: "1"});
                      updateData("mat_tien", {label: "khác", value: "khac"});
                      note = 
                        " - Nhà chung cư chỉ có 1 tầng nên chúng tôi tự động cài đặt tự động tầng bằng 1.\n" + 
                        " - Đối với nhà chung cư yếu tố mặt tiền không ảnh hưởng quá nhiều đến giá nên không cần phải chọn."
                  } 
                   setNote(note);
                }}
              >
              {label}
            </div>
            );
          })}
        </div>
      </div>
    );
  }

  if (selected === "giay-to-phap-ly") {
    const list = [
      "Sổ đỏ", 
      "Hợp đồng mua bán", 
      "Khác"
    ]

    return (
      <div className="box-option">
        <div className="list-option">
          {list.map((label, i) => (
              <div key={i} onClick={() => updateData("giay_to_phap_ly", {
                label: label,
                value: toSnakeCaseVN(label)
              })}>
                {label}
              </div>
            ))}         
        </div>      
      </div>
    );
  }

  if (selected === "vi-tri") {
    const list = [
      "Căn góc", 
      "Khu vực phát triển", 
      "Cạnh hồ", "Cạnh sông", 
      "Thuận tiện"
    ]

    return (
      <div className="box-option">
        <div className="list-option">
          {list.map((label, i) => (
              <div key={i} onClick={() => updateData("vi_tri", {
                label: label,
                value: toSnakeCaseVN(label)
              })}>
                {label}
              </div>
            ))}
        </div>      
      </div>
    );
  }

  if (selected === "mat-tien") {
    return (
      <div className="box-option">
        <div className="list-option">
          <input 
            type="text" 
            placeholder="Đơn vị m" 
            onChange={(e) => updateData("mat_tien", {
              label: e.target.value,
              value: e.target.value
            })}
          /> 
        </div>      
      </div>
    );
  }

  if (selected === "tinh-trang-nha") {
    const list = [
      "Mới", 
      "Bình Thường", 
      "Cũ"
    ]
    return (
      <div className="box-option">
        <div className="list-option">
          {list.map((label, i) => (
              <div key={i} onClick={()=>updateData("tinh_trang_nha", {
                label: label,
                value: toSnakeCaseVN(label)
              })}>
                {label}
              </div>
            ))}
        </div>      
      </div>
    );
  }

  if (selected === "tang") {
    const list = [
      1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19
    ]

    return (
      <div className="box-option">
        <div className="list-option">
          {list.map((label, i) => (
              <div key={i} onClick={()=>updateData("tang", {
                label: label,
                value: toSnakeCaseVN(label)
              })}>
                {label}
              </div>
            ))}
        </div>      
      </div>
    );
  }

  if (selected === "mo-ta") {
    const list = [
      "Khác", 
      "Bán gấp"
    ]
    return (
      <div className="box-option">
        <div className="list-option">
          {list.map((label, i) => (
              <div key={i} onClick={()=>updateData("mo_ta", {
                label: label,
                value: toSnakeCaseVN(label)
              })}>
                {label}
              </div>
            ))}
        </div>      
      </div>
    );
  }
  
  return null;
}

// Component hiển thị các lựa chọn đã chọn
function MainContent({ selectedData }) {
  return (
    <div className="main-content">
      <h3>Lựa chọn của bạn:</h3>
      {selectedData.dia_diem && <p><strong>Địa Điểm:</strong> {selectedData.dia_diem.label}</p>}
      {selectedData.so_phong_ngu && <p><strong>Số phòng ngủ:</strong> {selectedData.so_phong_ngu.label}</p>}      
      {selectedData.dien_tich && <p><strong>Diện tích:</strong> {selectedData.dien_tich.label} m²</p>}
      {selectedData.loai_nha && <p><strong>Loại nhà:</strong> {selectedData.loai_nha.label}</p>}
      {selectedData.giay_to_phap_ly && <p><strong>Giấy tờ pháp lý:</strong> {selectedData.giay_to_phap_ly.label}</p>}
      {selectedData.vi_tri && <p><strong>Vị trí:</strong> {selectedData.vi_tri.label}</p>}
      {selectedData.mat_tien && <p><strong>Mặt tiền:</strong> {selectedData.mat_tien.label}</p>}
      {selectedData.tinh_trang_nha && <p><strong>Tình trạng nhà:</strong> {selectedData.tinh_trang_nha.label}</p>}
      {selectedData.tang && <p><strong>Số tầng:</strong> {selectedData.tang.label}</p>}
      {selectedData.mo_ta && <p><strong>Mô tả:</strong> {selectedData.mo_ta.label}</p>}
      
      {/* Bạn có thể in ra JSON để gửi về backend */}
      {/* <pre>{JSON.stringify(selectedData, null, 2)}</pre> */}
    </div>
  );
}

function Note({message}){
  if (!message) {
    return (
    <div className="note">
      <strong>Ghi chú: </strong> {message}
    </div>
    );
  };
  return (
    <div className="note">
      <strong>Ghi chú: </strong>
      {message.split('\n').map((line, index) => (
        <React.Fragment key={index}>
          {line}
          <br />
        </React.Fragment>
      ))}
    </div>
  );
}

function Result({result, top_feature, onSubmit}){
  return (
    <div className="box-result">
      <div className="content-result">
        <button onClick={onSubmit}>Xem Kết quả</button>

        {result && (
          <>
            <div className="price">
              <strong>Giá dự đoán: </strong> {result}
            </div>
          </>
        )}       
      </div>

      <div className="box-feature">
        <h3>Top đặc trưng ảnh hưởng:</h3>
        <div className="top-feature">
          {top_feature && top_feature.map(([key, val]) => (
            <div key={key}>{key}: {val.toFixed(4)}</div>
          ))}
        </div>
      </div>
    </div>
  )
}

function App() {
  const [selectedOption, setSelectedOption] = useState(null);
  const [selectedData, setSelectedData] = useState({});
  const [note, setNote] = useState("");
  const [result, setResult] = useState(null)
  const [topFeature, setTopFeature] = useState(null)

  const updateData = (key, value) => {
    setSelectedData((prev) => ({...prev, [key]: value}));
  }

  const handleSubmit = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/du-lieu', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(selectedData)
      });

      if (response.ok) {
        const data = await response.json();
        setResult(data.price);
        setTopFeature(data.top_feature)
      } else {
        alert('Gửi thất bại!');
      }
    } catch (error) {
      console.error('Lỗi gửi dữ liệu:', error);
    }
  };

  return (
    <div className="app-container">
      <Header />
      <MainTitle />
      <div className="content-area">
        <SidebarNavigation onSelectOption={setSelectedOption}/>
        <SupportContent
          selected={selectedOption}
          updateData={updateData}
          setNote={setNote}
        /* {selectedOption && (
          <SupportContent 
            selected={selectedOption} 
            updateData={updateData}
            setNote={setNote}
          />
          )}      */
        />
        <div className="content-box">           
          <MainContent selectedData={selectedData}/>
          <Note message={note}/>
          <Result result={result} top_feature={topFeature} onSubmit={handleSubmit}/>
        </div>       
      </div>
    </div>
  );
}

export default App;