import pandas as pd

class Money_Time:
    def __init__(self):
        # Đơn giá theo loại xe (tính theo nghìn đồng)
        self.gia_theo_loai = {
            "Xe đạp": 2.0,
            "Xe máy": 5.0,
            "Xe điện": 3.5,
            "Ô tô": 10.0,
            "Xe tải": 15.0  
        }

    def set_gia(self, loai_xe, gia_moi):
        self.gia_theo_loai[loai_xe] = gia_moi

    def get_gia(self, loai_xe):
        return self.gia_theo_loai.get(loai_xe, 0)


class Info_Xe:
    def __init__(self, loai_xe, chu_xe, thoi_gian, bien_so=None):
        self.loai_xe = loai_xe
        self.chu_xe = chu_xe
        self.thoi_gian = thoi_gian
        self.bien_so = bien_so

    def tinh_tien(self, bang_gia: Money_Time):
        return self.thoi_gian * bang_gia.get_gia(self.loai_xe) * 1000

    def to_dict(self, bang_gia: Money_Time):
        return {
            "Chủ xe": self.chu_xe,
            "Loại xe": self.loai_xe,
            "Thời gian gửi (giờ)": self.thoi_gian,
            "Biển số": self.bien_so or "",
            "Thành tiền (VND)": self.tinh_tien(bang_gia)
        }


class QuanLyNhaXe:
    def __init__(self):
        self.bang_gia = Money_Time()
        self.ds_xe = []

    def them_xe(self, xe: Info_Xe):
        self.ds_xe.append(xe)

    def xoa_xe(self, chu_xe):
        self.ds_xe = [xe for xe in self.ds_xe if xe.chu_xe != chu_xe]

    def sua_thong_tin(self, chu_xe, **kwargs):
        for xe in self.ds_xe:
            if xe.chu_xe == chu_xe:
                xe.loai_xe = kwargs.get("loai_xe", xe.loai_xe)
                xe.thoi_gian = kwargs.get("thoi_gian", xe.thoi_gian)
                xe.bien_so = kwargs.get("bien_so", xe.bien_so)

    def cap_nhat_gia(self, loai_xe, gia_moi):
        self.bang_gia.set_gia(loai_xe, gia_moi)

    def xuat_du_lieu_excel(self, file_name="danh_sach_gui_xe.xlsx"):
        data = [xe.to_dict(self.bang_gia) for xe in self.ds_xe]
        df = pd.DataFrame(data)
        df.to_excel(file_name, index=False)
        print(f"Đã xuất dữ liệu ra file: {file_name}")

    def in_nguoi_gui_tren_20k(self):
        print("🔍 Danh sách người gửi xe trên 20.000đ:")
        for xe in self.ds_xe:
            tien = xe.tinh_tien(self.bang_gia)
            if tien > 20000:
                print(f"- {xe.chu_xe}: {tien} VND")



ql = QuanLyNhaXe()

ql.them_xe(Info_Xe("Xe đạp", "Nguyễn Văn A", 8))
ql.them_xe(Info_Xe("Xe máy", "Trần Thị B", 6, "29B1-123.45"))
ql.them_xe(Info_Xe("Ô tô", "Lê Văn C", 2, "30A-999.99"))
ql.them_xe(Info_Xe("Xe điện", "Phạm Thị D", 4))
ql.them_xe(Info_Xe("Xe tải", "Hoàng Minh E", 3))  # Thêm xe tải


ql.sua_thong_tin("Nguyễn Văn A", thoi_gian=8)


ql.cap_nhat_gia("Ô tô", 12)  

# Xuất danh sách người gửi xe trên 20k
ql.in_nguoi_gui_tren_20k()

# Ghi file Excel
ql.xuat_du_lieu_excel("data_gui_xe.xlsx")