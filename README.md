# Sudoku_CSP_AC3
## I] Cài đặt:
Clone project tới máy của bạn:
```bash
git clone https://github.com/TruongChiDien/Sudoku_CSP_AC3.git
cd Sudoku_CSP_AC3
```

Cài các module cần thiết (bỏ qua nếu đã có đủ):
```bash
pip3 install argparse itertool
```

## II] Thực thi:
Dự án này chỉ chạy trên Sudoku với bậc chẵn, kích thước của Sudoku bằng bậc^4
```bash
python solver.py --edge=<bậc> --sample=<số lượng Sudoku> --level<tỉ lệ được đánh số sẵn>
```
hoặc chạy với tham số mặc định là sudoku bậc 3, sample = 1 và level = 0.2 như sau:
```bash
python solver.py
```

Trong đó, edge = bậc = độ dài cạnh của 1 hình vuông nhỏ
sample = số lượng game mà bạn muốn tạo
level = tỉ lệ số ô được đánh số sẵn trong khoảng 0.1 tới 0.4 Nếu tỉ lệ này quá cao sẽ làm việc khởi tạo tốn nhiều thời gian và có thể tạo ra cách Sudoku không có lời giải. Còn nếu quá thấp thì thời gian giải sẽ tăng lên.

Kiểm tra tính đúng đắn của AC-3 bằng cách gọi lệnh sau
```bash
python Check_AC3.py
```
Chúng tôi sẽ tạo một Sudoku với cách cung đã nhất quán sẵn và cho AC3 chạy qua một phiên bản đã được thêm các giá trị khác vào bản chuẩn và so sánh kết quả với bản chuẩn.
