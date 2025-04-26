# -*- coding: utf-8 -*-
import tkinter
import customtkinter as ctk
import requests
import threading
import webbrowser
import platform
import json
import os
from io import BytesIO
from PIL import Image, ImageTk

try:
    import pyperclip
except ImportError:
    pyperclip = None

# --- Ayarlar ---
SETTINGS_FILE = "anime_app_settings.json"
DEFAULT_SETTINGS = {
    "theme": "dark", # Varsayılan tema
    "limit": 10, "auto_copy": True, "output_format": "BBCode",
    "include_score": True, "include_genres": True, "include_type": True, "include_year": True,
    "include_image_tag": False, "window_geometry": "1050x600"
}

# --- Ayar Yükleme/Kaydetme (Değişiklik Yok) ---
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f: loaded = json.load(f); settings = {**DEFAULT_SETTINGS, **loaded}
            for key, value in DEFAULT_SETTINGS.items(): settings.setdefault(key, value)
            settings.pop("sort_history_by", None)
            # Ensure theme is valid, fallback to default if not
            if settings.get("theme") not in ["dark", "light", "system"]:
                settings["theme"] = DEFAULT_SETTINGS["theme"]
            return settings
        except (json.JSONDecodeError, IOError) as e: print(f"Ayarlar yüklenemedi: {e}. Varsayılanlar kullanılacak."); return DEFAULT_SETTINGS.copy()
    return DEFAULT_SETTINGS.copy()
def save_settings(settings):
    try:
        settings.pop("sort_history_by", None)
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f: json.dump(settings, f, indent=4)
    except IOError as e: print(f"Ayarlar kaydedilemedi: {e}")

# --- Veritabanı İşlemleri (REMOVED) ---

# --- Yardımcı Fonksiyonlar (format_code Değişiklik Yok) ---
def format_code(data, format_type, include_score, include_genres, include_type, include_year, include_image_tag):
    if not data: return ""
    title=data.get('title', '?'); mal_url=data.get('mal_url', data.get('url', '#')); score=data.get('score'); year=data.get('year'); anime_type=data.get('type')
    genres_val=data.get('genres', ''); genres_list=[]
    if isinstance(genres_val, str): genres_list = [g.strip() for g in genres_val.split(',') if g.strip()]
    elif isinstance(genres_val, list):
         if genres_val and isinstance(genres_val[0], dict): genres_list = [g.get('name') for g in genres_val if g.get('name')]
         else: genres_list = genres_val
    image_url = None
    if 'images' in data and isinstance(data['images'], dict): image_url = data['images'].get('jpg', {}).get('large_image_url');
    if not image_url and 'images' in data and isinstance(data['images'], dict): image_url = data['images'].get('jpg', {}).get('image_url')
    if not image_url and 'images' in data and isinstance(data['images'], dict): image_url = data['images'].get('jpg', {}).get('small_image_url')
    elif 'image_url' in data: image_url = data['image_url']
    extra_parts=[]
    if include_score and score is not None: extra_parts.append(f"Puan: {score}")
    if include_genres and genres_list: extra_parts.append(f"Tür: {', '.join(genres_list)}")
    if include_type and anime_type: extra_parts.append(f"Tip: {anime_type}")
    if include_year and year: extra_parts.append(f"Yıl: {year}")
    extra_info_str = f" ({' | '.join(extra_parts)})" if extra_parts else ""
    formatted_code=""; image_tag=""
    if include_image_tag and image_url:
         if format_type == "BBCode": image_tag = f" [img]{image_url}[/img]"
         elif format_type == "Markdown": image_tag = f" ![]({image_url})"
    if format_type == "BBCode": formatted_code = f"[URL='{mal_url}']{title}[/URL]{extra_info_str}{image_tag}"
    elif format_type == "Markdown": formatted_code = f"[{title}]({mal_url}){extra_info_str}{image_tag}"
    else: formatted_code = f"{title} - {mal_url}"
    return formatted_code.strip()

# --- Geçmiş Düzenleme Penceresi (REMOVED) ---

# --- Ana Uygulama Sınıfı ---
class AnimeBBCodeApp(ctk.CTk):
    def __init__(self, settings):
        super().__init__(); self.settings = settings
        self.title("Gelişmiş Anime Link Oluşturucu"); self.geometry(self.settings.get("window_geometry", DEFAULT_SETTINGS["window_geometry"]))
        # Başlangıç temasını ayarlardan yükle
        ctk.set_appearance_mode(self.settings.get("theme", DEFAULT_SETTINGS["theme"]))
        # init_db() # Removed

        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(1, weight=1) # Sadece ana panel (row 1) genişlesin (Ayarlar paneli row'u kalktı)

        # --- Üst Panel ---
        top_frame = ctk.CTkFrame(self); top_frame.grid(row=0, column=0, padx=10, pady=(10,5), sticky="ew"); top_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(top_frame, text="Anime Adı:").grid(row=0, column=0, padx=5, pady=5); self.search_entry = ctk.CTkEntry(top_frame); self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew"); self.search_entry.bind("<Return>", self.start_search_thread)
        ctk.CTkLabel(top_frame, text="Limit:").grid(row=0, column=2, padx=(10, 5), pady=5); self.limit_var = ctk.StringVar(value=str(self.settings.get("limit", DEFAULT_SETTINGS["limit"]))); self.limit_entry = ctk.CTkEntry(top_frame, width=40, textvariable=self.limit_var); self.limit_entry.grid(row=0, column=3, padx=5, pady=5)
        self.search_button = ctk.CTkButton(top_frame, text="Ara", width=60, command=self.start_search_thread); self.search_button.grid(row=0, column=4, padx=5, pady=5)
        # --- DEĞİŞTİ: Ayar butonu artık tema değiştiriyor ---
        self.theme_button = ctk.CTkButton(top_frame, text="☀️/🌙", width=40, command=self.toggle_theme) # İkon yerine metin veya farklı ikon olabilir
        self.theme_button.grid(row=0, column=5, padx=5, pady=5)

        # --- Ayarlar Paneli (REMOVED) ---
        # self.settings_panel = ... removed ...

        # --- Orta Panel ---
        # Row indeksi 1 oldu (önce 2 idi)
        self.middle_frame = ctk.CTkFrame(self); self.middle_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew"); self.middle_frame.grid_columnconfigure(0, weight=4); self.middle_frame.grid_columnconfigure(1, weight=1); self.middle_frame.grid_rowconfigure(0, weight=1)
        results_frame = ctk.CTkFrame(self.middle_frame); results_frame.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="nsew"); results_frame.grid_rowconfigure(1, weight=1); results_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(results_frame, text="Arama Sonuçları:").grid(row=0, column=0, sticky="w", padx=5, pady=(5,0)); self.results_listbox = tkinter.Listbox(results_frame, height=10, bg="#2B2B2B", fg="white", selectbackground="#1F6AA5", borderwidth=0, highlightthickness=0, font=("Segoe UI", 10), selectmode=tkinter.BROWSE); self.results_listbox.grid(row=1, column=0, pady=5, padx=5, sticky="nsew"); self.results_listbox.bind("<<ListboxSelect>>", self.on_result_select)
        self.open_mal_search_button = ctk.CTkButton(results_frame, text="MAL Sayfasını Aç", command=self.open_mal_page_search, state="disabled"); self.open_mal_search_button.grid(row=2, column=0, pady=5, padx=5, sticky="ew")
        output_image_frame = ctk.CTkFrame(self.middle_frame); output_image_frame.grid(row=0, column=1, padx=(5, 0), pady=5, sticky="nsew"); output_image_frame.grid_columnconfigure(0, weight=0, minsize=260); output_image_frame.grid_columnconfigure(1, weight=1); output_image_frame.grid_rowconfigure(1, weight=1)
        self.image_label = ctk.CTkLabel(output_image_frame, text=""); self.image_label.grid(row=0, column=0, rowspan=4, padx=10, pady=10, sticky="nw"); self.current_ctk_image = None
        ctk.CTkLabel(output_image_frame, text="Oluşturulan Kod:").grid(row=0, column=1, sticky="nw", padx=5, pady=(5,0)); self.code_output_entry = ctk.CTkTextbox(output_image_frame, height=120); self.code_output_entry.grid(row=1, column=1, pady=5, padx=5, sticky="nsew")
        output_controls_frame = ctk.CTkFrame(output_image_frame); output_controls_frame.grid(row=2, column=1, pady=(0,5), padx=5, sticky="ew"); output_controls_frame.grid_columnconfigure(0, weight=1); button_container = ctk.CTkFrame(output_controls_frame, fg_color="transparent"); button_container.grid(row=0, column=1, sticky="e")
        self.auto_copy_var = ctk.BooleanVar(value=self.settings.get("auto_copy", DEFAULT_SETTINGS["auto_copy"])); self.auto_copy_checkbox = ctk.CTkCheckBox(button_container, text="Otomatik Kopyala", variable=self.auto_copy_var, command=self.update_setting_from_widget); self.auto_copy_checkbox.pack(side="right", padx=(10, 5))
        self.copy_button = ctk.CTkButton(button_container, text="Panoya Kopyala", command=self.copy_to_clipboard, state="disabled"); self.copy_button.pack(side="right", padx=5)
        self.output_format_var = ctk.StringVar(value=self.settings.get("output_format", DEFAULT_SETTINGS["output_format"])); self.format_segmented_button = ctk.CTkSegmentedButton(output_controls_frame, values=["BBCode", "Markdown"], variable=self.output_format_var, command=self.regenerate_code_if_selected); self.format_segmented_button.grid(row=0, column=0, padx=5, sticky="w")
        extra_info_frame = ctk.CTkFrame(output_image_frame); extra_info_frame.grid(row=3, column=1, pady=5, padx=5, sticky="ew"); extra_info_frame.grid_columnconfigure(0, weight=0); extra_info_frame.grid_columnconfigure(1, weight=0); extra_info_frame.grid_columnconfigure(2, weight=0)
        ctk.CTkLabel(extra_info_frame, text="Koda Ekle:").grid(row=0, column=0, columnspan=3, sticky="w", padx=(0,10), pady=(0,3))
        self.include_score_var = ctk.BooleanVar(value=self.settings.get("include_score", DEFAULT_SETTINGS["include_score"])); self.include_score_checkbox = ctk.CTkCheckBox(extra_info_frame, text="Puan", variable=self.include_score_var, command=self.regenerate_code_if_selected); self.include_score_checkbox.grid(row=1, column=0, padx=2, pady=2, sticky="w")
        self.include_genres_var = ctk.BooleanVar(value=self.settings.get("include_genres", DEFAULT_SETTINGS["include_genres"])); self.include_genres_checkbox = ctk.CTkCheckBox(extra_info_frame, text="Tür", variable=self.include_genres_var, command=self.regenerate_code_if_selected); self.include_genres_checkbox.grid(row=1, column=1, padx=2, pady=2, sticky="w")
        self.include_type_var = ctk.BooleanVar(value=self.settings.get("include_type", DEFAULT_SETTINGS["include_type"])); self.include_type_checkbox = ctk.CTkCheckBox(extra_info_frame, text="Tip", variable=self.include_type_var, command=self.regenerate_code_if_selected); self.include_type_checkbox.grid(row=1, column=2, padx=2, pady=2, sticky="w")
        self.include_year_var = ctk.BooleanVar(value=self.settings.get("include_year", DEFAULT_SETTINGS["include_year"])); self.include_year_checkbox = ctk.CTkCheckBox(extra_info_frame, text="Yıl", variable=self.include_year_var, command=self.regenerate_code_if_selected); self.include_year_checkbox.grid(row=2, column=0, padx=2, pady=2, sticky="w")
        self.include_image_tag_var = ctk.BooleanVar(value=self.settings.get("include_image_tag", DEFAULT_SETTINGS["include_image_tag"])); self.include_image_tag_checkbox = ctk.CTkCheckBox(extra_info_frame, text="Resim [img]", variable=self.include_image_tag_var, command=self.regenerate_code_if_selected); self.include_image_tag_checkbox.grid(row=2, column=1, padx=2, pady=2, sticky="w")

        # --- Alt Panel (History - REMOVED) ---

        # --- Durum Çubuğu ---
        # Row indeksi 2 oldu
        self.statusbar_frame = ctk.CTkFrame(self, height=25, fg_color="transparent"); self.statusbar_frame.grid(row=2, column=0, padx=10, pady=(0,5), sticky="ew"); self.statusbar_frame.grid_columnconfigure(0, weight=1); self.statusbar_frame.grid_columnconfigure(1, weight=0)
        self.status_label = ctk.CTkLabel(self.statusbar_frame, text="Hazır", anchor="w"); self.status_label.grid(row=0, column=0, sticky="w", padx=(5,0))
        self.website_label = ctk.CTkLabel(self.statusbar_frame, text="lexix.neocities.org", text_color="#26A0F5", cursor="hand2", anchor="e"); self.website_label.grid(row=0, column=1, sticky="e", padx=(0,10)); self.website_label.bind("<Button-1>", self.open_website)

        # --- Başlangıç İşlemleri ---
        self.search_results_data = []; self.selected_anime_data = None; self.protocol("WM_DELETE_WINDOW", self.on_closing)

    # --- Metodlar ---
    def load_image_async(self, url, callback):
        def _load():
            try:
                response = requests.get(url, stream=True, timeout=10); response.raise_for_status(); image_data = response.content
                pil_image = Image.open(BytesIO(image_data)); pil_image.thumbnail((250, 370))
                ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=pil_image.size); self.after(0, callback, ctk_image)
            except requests.exceptions.RequestException as e: print(f"Resim indirme hatası: {e}"); self.after(0, callback, None)
            except Exception as e: print(f"Resim işleme hatası: {e}"); self.after(0, callback, None)
        image_thread = threading.Thread(target=_load, daemon=True); image_thread.start()

    # --- toggle_settings_panel SİLİNDİ ---

    # --- YENİ METOD: Temayı Değiştirir ---
    def toggle_theme(self):
        """Açık ve koyu tema arasında geçiş yapar."""
        current_mode = ctk.get_appearance_mode()
        if current_mode.lower() == "dark":
            new_mode = "light"
        else: # light veya system ise dark yap
            new_mode = "dark"
        ctk.set_appearance_mode(new_mode)
        self.settings["theme"] = new_mode # Ayarı güncelle
        self.update_status(f"Tema '{new_mode}' olarak değiştirildi.", "info")

    # --- update_setting_from_widget GÜNCELLENDİ (tema kısmı yok) ---
    def update_setting_from_widget(self, *args):
        # theme artık toggle_theme içinde güncelleniyor
        self.settings["limit"] = self.limit_var.get(); self.settings["auto_copy"] = self.auto_copy_var.get(); self.settings["output_format"] = self.output_format_var.get()
        self.settings["include_score"] = self.include_score_var.get(); self.settings["include_genres"] = self.include_genres_var.get()
        self.settings["include_type"] = self.include_type_var.get(); self.settings["include_year"] = self.include_year_var.get(); self.settings["include_image_tag"] = self.include_image_tag_var.get()

    # --- Diğer Metodlar (Değişiklik Yok) ---
    def start_search_thread(self, event=None):
        query = self.search_entry.get().strip(); limit_str = self.limit_var.get().strip()
        if not query: self.update_status("Lütfen aranacak bir anime adı girin.", "warning"); return
        try: limit = int(limit_str); limit = max(1, min(limit, 25))
        except ValueError: limit = 10
        self.limit_var.set(str(limit)); self.settings["limit"] = str(limit)
        self.search_button.configure(state="disabled", text="..."); self.search_entry.configure(state="disabled"); self.results_listbox.delete(0, "end")
        self.clear_output_and_image(); self.disable_result_actions(); self.update_status(f"'{query}' aranıyor (limit: {limit})...")
        search_thread = threading.Thread(target=self.search_anime, args=(query, limit), daemon=True); search_thread.start()
    def search_anime(self, query, limit):
        jikan_url = f"https://api.jikan.moe/v4/anime?q={query}&limit={limit}&sfw"
        try: response = requests.get(jikan_url, timeout=20); response.raise_for_status(); data = response.json(); self.after(0, self.display_search_results, data.get('data', []))
        except requests.exceptions.Timeout: self.after(0, self.show_search_error, "API isteği zaman aşımına uğradı.")
        except requests.exceptions.HTTPError as e: status_code = e.response.status_code; error_msg = f"API hatası: {status_code}"; self.after(0, self.show_search_error, error_msg)
        except requests.exceptions.RequestException as e: self.after(0, self.show_search_error, f"Ağ hatası: {e}")
        except json.JSONDecodeError: self.after(0, self.show_search_error, "API'den geçersiz yanıt alındı.")
        except Exception as e: self.after(0, self.show_search_error, f"Beklenmedik hata: {e}")
        finally: self.after(0, self.enable_search_controls)
    def display_search_results(self, results):
        self.results_listbox.delete(0, "end"); self.search_results_data = results; self.selected_anime_data = None; self.disable_result_actions()
        if not results: self.update_status("Arama sonucu bulunamadı.", "info"); return
        for i, anime in enumerate(results): title = anime.get('title', '?'); year = anime.get('year', '?'); score = anime.get('score'); display_text = f"{title} ({year}){' - '+str(score) if score else ''}"; self.results_listbox.insert("end", display_text)
        self.update_status(f"{len(results)} sonuç bulundu. Lütfen birini seçin.", "info")
    def show_search_error(self, error_message): self.update_status(f"Hata: {error_message}", "error")
    def enable_search_controls(self): self.search_button.configure(state="normal", text="Ara"); self.search_entry.configure(state="normal")
    def disable_result_actions(self): self.copy_button.configure(state="disabled"); self.open_mal_search_button.configure(state="disabled"); self.clear_output_and_image()
    def on_result_select(self, event=None):
        selected_indices = self.results_listbox.curselection()
        if not selected_indices: self.disable_result_actions(); return
        selected_index = selected_indices[0]
        if 0 <= selected_index < len(self.search_results_data):
            self.selected_anime_data = self.search_results_data[selected_index]
            image_url = self.selected_anime_data.get('images', {}).get('jpg', {}).get('large_image_url')
            if not image_url: image_url = self.selected_anime_data.get('images', {}).get('jpg', {}).get('image_url')
            if not image_url: image_url = self.selected_anime_data.get('images', {}).get('jpg', {}).get('small_image_url')
            if image_url: self.update_status("Resim yükleniyor...", "info"); self.load_image_async(image_url, self.update_image_label)
            else: self.clear_output_and_image(clear_image=True)
            self.generate_code_and_update_ui(); self.copy_button.configure(state="normal")
            if self.selected_anime_data.get('url'): self.open_mal_search_button.configure(state="normal")
        else: self.selected_anime_data = None; self.disable_result_actions()
    def generate_code_and_update_ui(self, data=None):
        source_data = data if data is not None else self.selected_anime_data
        if not source_data: self.code_output_entry.delete("1.0", "end"); return
        format_type=self.output_format_var.get(); include_score=self.include_score_var.get(); include_genres=self.include_genres_var.get(); include_type=self.include_type_var.get(); include_year=self.include_year_var.get(); include_image=self.include_image_tag_var.get()
        self.update_setting_from_widget(); generated_code = format_code(source_data, format_type, include_score, include_genres, include_type, include_year, include_image)
        self.code_output_entry.delete("1.0", "end"); self.code_output_entry.insert("1.0", generated_code)
        if data is None: self.update_status("Kod oluşturuldu.", "success")
        if self.auto_copy_var.get() and generated_code and data is None: self.copy_to_clipboard()
    def regenerate_code_if_selected(self, *args):
        if self.selected_anime_data: self.generate_code_and_update_ui(self.selected_anime_data)
        else: self.code_output_entry.delete("1.0", "end"); self.clear_output_and_image()
    def update_image_label(self, ctk_image):
        if ctk_image: self.image_label.configure(image=ctk_image); self.current_ctk_image = ctk_image
        else: self.image_label.configure(image=None); self.current_ctk_image = None
    def clear_output_and_image(self, clear_image=True, clear_output=True):
        if clear_image: self.image_label.configure(image=None); self.current_ctk_image = None
        if clear_output: self.code_output_entry.delete("1.0", "end")
    def copy_to_clipboard(self):
        code_to_copy = self.code_output_entry.get("1.0", "end-1c").strip()
        if not code_to_copy: self.update_status("Kopyalanacak kod yok.", "warning"); return
        try:
            if pyperclip: pyperclip.copy(code_to_copy); self.update_status("Kod panoya kopyalandı!", "success"); return
            self.clipboard_clear(); self.clipboard_append(code_to_copy); self.update_idletasks(); self.update_status("Kod panoya kopyalandı! (tkinter)", "success")
        except Exception as e: self.update_status(f"Panoya kopyalama hatası: {e}", "error")
    def open_mal_page_search(self):
         if self.selected_anime_data and self.selected_anime_data.get('url'): webbrowser.open(self.selected_anime_data['url'])
         else: self.update_status("Açılacak geçerli bir MAL URL'si bulunamadı.", "warning")
    def open_website(self, event=None):
        try: webbrowser.open("https://lexix.neocities.org"); self.update_status("Web sitesi açılıyor...", "info")
        except Exception as e: self.update_status(f"Web sitesi açılamadı: {e}", "error")
    def update_status(self, message, level="info"):
        color_map = { "info": ("white", "black"), "success": ("#00E676", "#00C853"), "warning": ("#FFA726", "#FF9100"), "error": ("#FF5252", "#FF1744") }
        current_theme = ctk.get_appearance_mode().lower(); text_color = color_map.get(level, ("white", "black"))[1 if current_theme == "light" else 0]
        self.status_label.configure(text=message, text_color=text_color); self.update_idletasks()
    def on_closing(self):
        self.settings["window_geometry"] = self.geometry(); self.update_setting_from_widget(); save_settings(self.settings)
        print("Ayarlar kaydedildi. Uygulama kapatılıyor."); self.destroy()

# --- Uygulamayı Başlatma ---
if __name__ == "__main__":
    if platform.system() == "Windows": os.system("chcp 65001 > nul")
    current_settings = load_settings()
    app = AnimeBBCodeApp(current_settings)
    app.mainloop()