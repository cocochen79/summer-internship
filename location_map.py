import json
import folium

# ========================================
# 1. 讀取南港區里界
# ========================================

with open("./mapdata/nangangtsunli.geojson", "r", encoding="utf-8") as f:
    geojson_data = json.load(f)


# ========================================
# 2. 讀取廟宇點位 GeoJSON
# ========================================

with open("./mapdata/location3.geojson", "r", encoding="utf-8") as f:
    temple_data = json.load(f)


# ========================================
# 3. 建立 Folium 地圖
# ========================================

m = folium.Map(
    location=[25.04, 121.619906], zoom_start=13
)


# ========================================
# 4. 加入南港區村里界
# ========================================

folium.GeoJson(
    geojson_data,
    name="南港區村里界"
).add_to(m)


# ========================================
# ★ 5. 建立「廟宇點位」圖層
# ========================================

temple_layer = folium.FeatureGroup(
    name="廟宇點位"
)

temple_layer.add_to(m)


# ========================================
# 6. 廟宇的連結
# ========================================

temple_links = {

    "聖媽廟": {
        "streetview": [
            "https://www.mapillary.com/app/?pKey=2305742023593634",
            "https://www.mapillary.com/app/?pKey=1806538350728187",
            "https://www.mapillary.com/app/?pKey=3035540040118246"
        ],

        "image": "https://drive.google.com/drive/folders/1ftPm3wqkKAN-BIi100Mn628uT7ndZqjz?usp=sharing"
    },


    "德聖公廟": {
        "streetview": "https://www.mapillary.com/app/?pKey=2513045589176437",

        "image": "https://drive.google.com/drive/folders/1wpe7UkYNtPYCHR8g4A91HpCCUrgbymvl?usp=sharing"
    },


    "百靈公廟": {
        "streetview": "https://www.mapillary.com/app/?pKey=1187181414486629",

        "image": "https://drive.google.com/drive/folders/17zl96t3qgnnVq6WP0xYrrT6wbDxERHGY?usp=sharing"
    },


    "萬善堂": {
        "image": "https://drive.google.com/drive/folders/1aMBtumHabAoKAzTWiBFAEUfGnDozE7Am?usp=sharing"
    },


    "昭安宮萬善祠": {
        "image": "https://drive.google.com/drive/folders/1A1I6gFjoBQ6zBDTJ1fu2OogpqxRPwaRP?usp=sharing"
    }
}


# ========================================
# 7. 開始建立廟宇 Marker
# ========================================

for feature in temple_data["features"]:

    properties = feature["properties"]

    name = properties["廟宇名稱"]

    coordinates = feature["geometry"]["coordinates"]

    lon = coordinates[0]
    lat = coordinates[1]


    # ====================================
    # 取得這間廟的連結
    # ====================================

    links = temple_links.get(name, {})

    streetview_urls = links.get("streetview", [])

    image_url = links.get("image", "")


    # ====================================
    # 建立按鈕
    # ====================================

    buttons = ""

    # ------------------------------------
    # Mapillary 街景
    # ------------------------------------

    if streetview_urls:

        # 聖媽廟有三個 Mapillary 連結
        if name == "聖媽廟":

            buttons += """
            <div style="display:inline-block; margin:3px;">

                <button
                    onclick="
                    this.nextElementSibling.style.display =
                    this.nextElementSibling.style.display === 'none'
                    ? 'block' : 'none';
                    "
                    style="
                    padding:6px 12px;
                    background:#f0f0f0;
                    color:#333;
                    border:1px solid #ccc;
                    border-radius:6px;
                    cursor:pointer;">
                    Mapillary 街景
                </button>

                <div style="display:none; margin-top:5px;">
            """


            for i, url in enumerate(streetview_urls, 1):

                buttons += f"""
                <a href="{url}"
                   target="_blank"
                   style="
                   display:block;
                   padding:5px 10px;
                   margin:3px 0;
                   color:#333;
                   text-decoration:none;">
                   影像連結 {i}
                </a>
                """


            buttons += """
                </div>
            </div>
            """


        # 其他廟宇只有一個 Mapillary
        else:

            buttons += f"""
            <a href="{streetview_urls}"
               target="_blank"
               style="
               display:inline-block;
               padding:6px 12px;
               margin:3px;
               background:#f0f0f0;
               color:#333;
               text-decoration:none;
               border:1px solid #ccc;
               border-radius:6px;">
               Mapillary 街景
            </a>
            """


    # ------------------------------------
    # 廟宇影像
    # ------------------------------------

    if image_url:

        buttons += f"""
        <a href="{image_url}"
           target="_blank"
           style="
           display:inline-block;
           padding:6px 12px;
           margin:3px;
           background:#f0f0f0;
           color:#333;
           text-decoration:none;
           border:1px solid #ccc;
           border-radius:6px;">
           廟宇影像
        </a>
        """


    # ====================================
    # 8. 建立 Popup
    # ====================================

    popup_html = f"""
    <div style="width:250px;">

        <h4>{name}</h4>

        <p>
        <b>地址：</b>{properties.get("地址", "")}<br>
        <b>主祀：</b>{properties.get("主祀", "")}<br>
        <b>建立與擴建時間：</b>{properties.get("建立與擴建時間", "")}<br>
        </p>

        <div style="margin-top:10px;">
            {buttons}
        </div>

    </div>
    """


    # ====================================
    # 9. 建立 Marker
    # ====================================

    folium.Marker(
        location=[lat, lon],

        popup=folium.Popup(
            popup_html,
            max_width=350
        ),

        tooltip=name
    ).add_to(temple_layer)


# ========================================
# 10. 加入圖層控制
# ========================================

folium.LayerControl().add_to(m)


# ========================================
# 11. 儲存地圖
# ========================================

m.save("./content/map.html")


# ========================================
# 12. 顯示地圖
# ========================================

m