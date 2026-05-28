import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
import numpy as np

# Pustaka tambahan untuk permodelan data
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans

# =====================================
# CONFIG PAGE
# =====================================

st.set_page_config(
    page_title="EDUVERA // Analytics Platform",
    page_icon="📊",
    layout="wide"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #161B22;
}

h1, h2, h3 {
    color: #58A6FF;
}

.stMetric {
    background-color: #161B22;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #30363D;
}

[data-testid="stDataFrame"] {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# SIDEBAR UPLOAD
# =====================================

st.sidebar.title("📂 Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload Dataset",
    type=["csv", "xlsx", "xls"]
)

# =====================================
# LOAD DATASET
# =====================================

try:

    # =====================================
    # JIKA USER UPLOAD FILE
    # =====================================

    if uploaded_file is not None:

        file_name = uploaded_file.name

        # CSV
        if file_name.endswith(".csv"):

            df = pd.read_csv(
                uploaded_file,
                encoding="utf-8"
            )

        # EXCEL
        elif (
            file_name.endswith(".xlsx")
            or
            file_name.endswith(".xls")
        ):

            df = pd.read_excel(
                uploaded_file
            )

        st.sidebar.success(
            "✅ Dataset berhasil diupload!"
        )

    # =====================================
    # DATASET DEFAULT (SUDAH DISESUAIKAN)
    # =====================================

    else:

        df = pd.read_csv(
            "data.csv"
        )

    # =====================================
    # HAPUS KOLOM KOSONG
    # =====================================

    df = df.loc[
        :,
        ~df.columns.str.contains("^Unnamed")
    ]

    # =====================================
    # VALIDASI DATASET
    # =====================================

    required_columns = [
        "Provinsi",
        "Sekolah",
        "Siswa"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:

        st.error("""
        ❌ Dataset wajib mempunyai minimal:

        - Provinsi
        - Sekolah
        - Siswa

        Jika tidak ada kolom di atas,
        maaf dashboard ini tidak dapat membaca dataset.
        """)

        st.stop()

except Exception as e:

    st.error(
        f"❌ Error membaca dataset: {e}"
    )

    st.stop()

# =====================================
# SIDEBAR MENU
# =====================================

st.sidebar.title("📌 Navigation")

menu = st.sidebar.radio(
    "Pilih Menu",
    [
        "Main Dashboard",
        "Search Region",
        "Region Ranking",
        "Distribution Map",
        "Trend Projection", 
        "Density Clustering"  
    ]
)

# =====================================
# KOORDINAT PROVINSI
# =====================================

koordinat = {
    "Prov. D.K.I. Jakarta": [-6.2, 106.8],
    "Prov. Jawa Barat": [-6.91, 107.61],
    "Prov. Jawa Tengah": [-7.15, 110.14],
    "Prov. Jawa Timur": [-7.53, 112.23],
    "Prov. D.I. Yogyakarta": [-7.80, 110.36],
    "Prov. Banten": [-6.12, 106.15],
    "Prov. Bali": [-8.65, 115.21],
    "Prov. Aceh": [5.55, 95.32],
    "Prov. Sumatera Utara": [3.59, 98.67],
    "Prov. Sumatera Barat": [-0.95, 100.35],
    "Prov. Riau": [0.51, 101.45],
    "Prov. Kepulauan Riau": [0.92, 104.45],
    "Prov. Jambi": [-1.61, 103.61],
    "Prov. Bengkulu": [-3.79, 102.26],
    "Prov. Lampung": [-5.45, 105.26],
    "Prov. Kalimantan Barat": [-0.02, 109.34],
    "Prov. Kalimantan Tengah": [-2.21, 113.92],
    "Prov. Kalimantan Selatan": [-3.31, 114.59],
    "Prov. Kalimantan Timur": [0.5, 117.15],
    "Prov. Sulawesi Selatan": [-5.14, 119.41],
    "Prov. Sulawesi Utara": [1.49, 124.84],
    "Prov. Papua": [-2.54, 140.71],
    "Prov. Papua Barat": [-0.86, 134.08],
    "Prov. Nusa Tenggara Barat": [-8.58, 116.10],
    "Prov. Nusa Tenggara Timur": [-10.17, 123.58]
}

# =====================================
# MAIN DASHBOARD
# =====================================

if menu == "Main Dashboard":

    st.title("📊 EDUVERA")
    st.caption("Interactive Education Data Hub Indonesia")

    st.write("""
    Platform pemantauan data interaktif statistik pendidikan nasional.

    Fitur Utama:
    - 🔍 Search Region (Pencarian Data Spesifik)
    - 🏆 Region Ranking (Pemeringkatan Kontributor)
    - 🗺️ Distribution Map (Peta Sebaran Nasional)
    - 📈 Trend Projection & Density Clustering (Analisis Data Lanjutan)
    """)

    # =====================================
    # STATISTIK
    # =====================================

    st.subheader("📌 Overview Data")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Wilayah (Provinsi)",
            len(df)
        )

    with col2:
        st.metric(
            "Total Satuan Pendidikan",
            f"{int(df['Sekolah'].sum()):,}"
        )

    with col3:
        st.metric(
            "Total Peserta Didik",
            f"{int(df['Siswa'].sum()):,}"
        )

    # =====================================
    # PILIH CHART
    # =====================================

    st.subheader("📈 Visualisasi Data")

    chart_type = st.selectbox(
        "Pilih Jenis Grafik",
        [
            "Bar Chart",
            "Pie Chart",
            "Line Chart",
            "Scatter Chart"
        ]
    )

    # =====================================
    # BAR CHART
    # =====================================

    if chart_type == "Bar Chart":

        fig = px.bar(
            df,
            x="Provinsi",
            y="Sekolah",
            color="Sekolah",
            title="Jumlah Sekolah per Provinsi"
        )

    # =====================================
    # PIE CHART
    # =====================================

    elif chart_type == "Pie Chart":

        fig = px.pie(
            df,
            names="Provinsi",
            values="Sekolah",
            title="Persentase Distribusi Sekolah"
        )

    # =====================================
    # LINE CHART
    # =====================================

    elif chart_type == "Line Chart":

        fig = px.line(
            df,
            x="Provinsi",
            y="Sekolah",
            markers=True,
            title="Tren Kuantitas Sekolah"
        )

    # =====================================
    # SCATTER CHART
    # =====================================

    elif chart_type == "Scatter Chart":

        fig = px.scatter(
            df,
            x="Sekolah",
            y="Siswa",
            hover_name="Provinsi",
            color="Siswa",
            size="Sekolah",
            title="Korelasi Satuan Pendidikan vs Peserta Didik"
        )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================
# SEARCH REGION
# =====================================

elif menu == "Search Region":

    st.title("🔍 Search Region")

    search = st.text_input(
        "Masukkan Nama Provinsi"
    )

    filtered_df = df[
        df["Provinsi"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

    if filtered_df.empty:

        st.warning(
            "⚠️ Data wilayah tidak ditemukan!"
        )

        st.stop()

    provinsi = st.selectbox(
        "Pilih Hasil Spesifik",
        filtered_df["Provinsi"]
    )

    data_provinsi = df[
        df["Provinsi"] == provinsi
    ]

    st.subheader(
        f"📋 Profil Data {provinsi}"
    )

    st.dataframe(
        data_provinsi,
        use_container_width=True
    )

    numeric_columns = df.select_dtypes(
        include=['int64', 'float64']
    ).columns

    st.subheader("📊 Indikator Statistik")

    cols = st.columns(3)

    for i, col in enumerate(numeric_columns):

        with cols[i % 3]:

            st.metric(
                label=col,
                value=f"{int(data_provinsi[col].values[0]):,}"
            )

    st.subheader("🗺️ Geokordinat Wilayah")

    if provinsi in koordinat:

        lat = koordinat[provinsi][0]
        lon = koordinat[provinsi][1]

        m = folium.Map(
            location=[lat, lon],
            zoom_start=7,
            tiles="CartoDB positron"
        )

        popup_text = f"""
        <b>{provinsi}</b><br>
        Sekolah: {data_provinsi['Sekolah'].values[0]:,}<br>
        Siswa: {data_provinsi['Siswa'].values[0]:}
        """

        folium.Marker(
            [lat, lon],
            popup=popup_text,
            tooltip=provinsi,
            icon=folium.Icon(
                color="red",
                icon="info-sign"
            )
        ).add_to(m)

        st_folium(
            m,
            width=1200,
            height=500
        )

# =====================================
# REGION RANKING
# =====================================

elif menu == "Region Ranking":

    st.title("🏆 Region Ranking")

    numeric_columns = df.select_dtypes(
        include=['int64', 'float64']
    ).columns

    ranking_column = st.selectbox(
        "Pilih Parameter Urutan",
        numeric_columns
    )

    ranking_df = df.sort_values(
        by=ranking_column,
        ascending=False
    ).reset_index(drop=True)

    ranking_df.index = ranking_df.index + 1

    ranking_df.insert(
        0,
        "Peringkat",
        ranking_df.index
    )

    st.subheader("🥇 Tiga Wilayah Tertinggi")

    top3 = ranking_df.head(3)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.success(
            f"🥇 {top3.iloc[0]['Provinsi']}"
        )

    with c2:
        st.info(
            f"🥈 {top3.iloc[1]['Provinsi']}"
        )

    with c3:
        st.warning(
            f"🥉 {top3.iloc[2]['Provinsi']}"
        )

    st.subheader(
        f"📋 Tabel Peringkat Berdasarkan {ranking_column}"
    )

    st.dataframe(
        ranking_df[
            [
                "Peringkat",
                "Provinsi",
                ranking_column
            ]
        ],
        use_container_width=True
    )

    fig = px.bar(
        ranking_df.head(10),
        x="Provinsi",
        y=ranking_column,
        color=ranking_column,
        title=f"Sepuluh Wilayah Teratas ({ranking_column})"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================
# DISTRIBUTION MAP
# =====================================

elif menu == "Distribution Map":

    st.title("🗺️ Distribution Map")

    st.info("""
    📌 Catatan Teknis:
    Satuan Pendidikan Luar Negeri tidak diikutsertakan dalam visualisasi peta nasional.
    """)

    df_map = df.copy()

    df_map = df_map[
        ~df_map["Provinsi"].str.contains(
            "Luar Negeri",
            case=False,
            na=False
        )
    ]

    provinsi_pilih = st.selectbox(
        "📍 Fokus Wilayah Peninjauan",
        ["Nasional (Seluruh Indonesia)"] + list(df_map["Provinsi"])
    )

    center_lat = -2.5
    center_lon = 118
    zoom = 5

    if provinsi_pilih != "Nasional (Seluruh Indonesia)":

        if provinsi_pilih in koordinat:

            center_lat = koordinat[
                provinsi_pilih
            ][0]

            center_lon = koordinat[
                provinsi_pilih
            ][1]

            zoom = 7

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        tiles="CartoDB positron"
    )

    for index, row in df_map.iterrows():

        prov = row["Provinsi"]

        if prov in koordinat:

            lat = koordinat[prov][0]
            lon = koordinat[prov][1]

            popup_text = f"""
            <b>{prov}</b><br>
            Sekolah: {row['Sekolah']:,}<br>
            Siswa: {row['Siswa']:,}
            """

            color = "blue"

            if prov == provinsi_pilih:
                color = "red"

            folium.CircleMarker(
                location=[lat, lon],
                radius=12,
                popup=popup_text,
                tooltip=prov,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7
            ).add_to(m)

    st_folium(
        m,
        width=1200,
        height=700
    )

# =====================================
# TREND PROJECTION
# =====================================
elif menu == "Trend Projection":
    st.title("📈 Trend Projection")
    st.write("Pemodelan statistik linear untuk memproyeksikan kapasitas kuantitas target siswa masa depan berdasarkan skala infrastruktur.")

    X = df[['Sekolah']].values
    y = df['Siswa'].values

    model = LinearRegression()
    model.fit(X, y)

    st.subheader("⚙️ Parameter Proyeksi")
    input_sekolah = st.number_input("Rencana Kuantitas Penambahan Satuan Pendidikan Baru:", min_value=1, value=int(df['Sekolah'].median()))

    prediksi_siswa = model.predict([[input_sekolah]])

    st.metric(
        label=f"Proyeksi Estimasi Tampung Murid ({input_sekolah} Sekolah)",
        value=f"{int(prediksi_siswa[0]):,}"
    )

    st.subheader("📊 Garis Tren Proyeksi Linier")
    df['Prediksi_Siswa'] = model.predict(X)
    
    fig_pred = px.scatter(df, x='Sekolah', y='Siswa', hover_name='Provinsi', title='Korelasi Aktual Kontra Garis Proyeksi')
    fig_pred.add_traces(px.line(df, x='Sekolah', y='Prediksi_Siswa').data[0])
    fig_pred.data[1].line.color = 'red'
    
    st.plotly_chart(fig_pred, use_container_width=True)

# =====================================
# DENSITY CLUSTERING
# =====================================
elif menu == "Density Clustering":
    st.title("📊 Density Clustering")

    st.warning("""
    ⚠️ **CATATAN ANALISIS:** Pengelompokkan wilayah ini mengukur **Rasio Kepadatan Kuantitatif (Jumlah Siswa per Sekolah)**. Langkah ini diterapkan guna menjaga objektivitas hasil klasifikasi antar-daerah tanpa diskriminasi dominasi populasi wilayah.
    """)

    df['Rasio_Siswa_Sekolah'] = df['Siswa'] / df['Sekolah'].replace(0, 1)
    features = df[['Rasio_Siswa_Sekolah']].values

    kmeans = KMeans(n_clusters=3, random_state=42)
    df['Cluster_ID'] = kmeans.fit_predict(features)

    cluster_means = df.groupby('Cluster_ID')['Rasio_Siswa_Sekolah'].mean().sort_values().index
    
    cluster_map = {
        cluster_means[0]: '🔴 Kapasitas Longgar (Rasio Kepadatan Rendah)', 
        cluster_means[1]: '🟡 Kapasitas Ideal (Proporsional)', 
        cluster_means[2]: '🟢 Kapasitas Padat (Kritis)'
    }
    df['Status Kepadatan'] = df['Cluster_ID'].map(cluster_map)

    st.subheader("💡 Ringkasan Klasterisasi")
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        st.metric("🟢 Wilayah Padat", f"{len(df[df['Status Kepadatan'] == cluster_map[cluster_means[2]]])} Wilayah")
    with col_c2:
        st.metric("🟡 Wilayah Ideal", f"{len(df[df['Status Kepadatan'] == cluster_map[cluster_means[1]]])} Wilayah")
    with col_c3:
        st.metric("🔴 Wilayah Longgar", f"{len(df[df['Status Kepadatan'] == cluster_map[cluster_means[0]]])} Wilayah")

    st.subheader("📋 Matriks Klasifikasi Beban Wilayah")
    tab1, tab2, tab3 = st.tabs(["🟢 Kluster Kritis/Padat", "🟡 Kluster Proporsional", "🔴 Kluster Longgar"])
    
    with tab1:
        st.markdown("""
        ### 🟢 Kategori: Beban Satuan Pendidikan Tinggi/Padat
        * **🏫 Infrastruktur Gedung:** Rasio ketersediaan sarana fisik sekolah lebih rendah dibanding pertumbuhan populasi usia sekolah setempat.
        * **👥 Kondisi Peserta Didik:** Satu institusi melayani jumlah siswa dalam volume kolektif yang sangat padat.
        * **📢 Kebijakan Rekomendasi:** Wilayah dalam segmen ini diprioritaskan utama untuk akselerasi pembangunan sarana fisik kelas atau sekolah baru.
        """)
    with tab2:
        st.markdown("""
        ### 🟡 Kategori: Beban Satuan Pendidikan Proporsional
        * **🏫 Infrastruktur Gedung:** Distribusi dan kuantitas unit sarana fisik mencukupi ruang akomodasi belajar.
        * **👥 Kondisi Peserta Didik:** Distribusi jumlah siswa per sekolah berada pada batas rata-rata standardisasi operasional yang ideal.
        * **📢 Kebijakam Rekomendasi:** Optimalisasi kualitas fasilitas pendukung eksisting serta peningkatan program mutu tenaga pendidik.
        """)
    with tab3:
        st.markdown("""
        ### 🔴 Kategori: Beban Satuan Pendidikan Longgar
        * **🏫 Infrastruktur Gedung:** Sarana fisik institusi pendidikan tersebar luas menjangkau titik demografi terjauh.
        * **👥 Kondisi Peserta Didik:** Rasio siswa per sekolah cenderung minimal imbas dari struktur sebaran populasi penduduk setempat yang renggang.
        * **📢 Kebijakan Rekomendasi:** Fokus pada pemerataan aksesibilitas moda transportasi murid terintegrasi menuju sekolah.
        """)

    st.write("---")
    st.subheader("📊 Tabel Hasil Klasifikasi Lengkap")

    df_tabel = df.copy().sort_values(by='Rasio_Siswa_Sekolah', ascending=False)
    
    df_tabel = df_tabel.reset_index(drop=True)
    df_tabel.index = df_tabel.index + 1  
    
    kolom_tampil = list(df_tabel.columns)
    st.dataframe(df_tabel[kolom_tampil], use_container_width=True)

    fig_clust = px.scatter(
        df, 
        x="Sekolah", 
        y="Siswa", 
        size="Rasio_Siswa_Sekolah",
        color="Status Kepadatan",
        hover_name="Provinsi",
        title="Matriks Sebaran Kluster Pemetaan Kepadatan (Skala Volume Lingkaran Merepresentasikan Rasio Kepadatan)",
        color_discrete_map={
            cluster_map[cluster_means[2]]: '#2ecc71', 
            cluster_map[cluster_means[1]]: '#f1c40f', 
            cluster_map[cluster_means[0]]: '#e74c3c'  
        }
    )
    st.plotly_chart(fig_clust, use_container_width=True)
