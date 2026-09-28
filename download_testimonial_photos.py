#!/usr/bin/env python3
"""Download LeadMaker testimonial photos with clean filenames."""

import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "images" / "testimonials"
CDN = "https://cdn.prod.website-files.com/63e7aed25b939f1b4889b50d/"

DOWNLOADS = {
    "jordan-carter.jpeg": "69cd47c0b5edf72e04d51f55_photo_upload_d2048577af3047a235fc21f1580a2a34%3Dface.jpeg",
    "dan-frickey.webp": "69781e6c29335a4e5f21f8c6_images.webp",
    "terri-wiksten.webp": "69400a2bfa0f5330c37c63cb_Terri_Wiksten_295x295w-1.webp",
    "oscar-mendoza.jpg": "686d5481002835985556b65d_WhatsApp%20Image%202025-07-08%20at%2010.36.03_afbb1fb0.jpg",
    "randy-gray.jpeg": "68137f5486bb710e47117a20_1718308255474.jpeg",
    "emiliano-basso.jpeg": "68137d5ee3176ee0fff3a257_1740523711170.jpeg",
    "ginger-chien.jpg": "68141e8e824e97ed0ff0a76d_1598284551284.jpg",
    "mark-tanyag.jpeg": "672c8186e82520e3959e207c_1516888810785.jpeg",
    "jae-choi.jpg": "672c810bb9e9c4e27cfbf9c9_Jae_Choi.jpg",
    "maebel-reliquias.jpeg": "672c805f9adabb3768a29402_maebel%20reliquias.jpeg",
    "bo-ward.jpg": "6734ca9c44e04f62c479cb5f_bo-ward.jpg",
    "eric-bordeos.jpeg": "672c7ef90042ab195adc2a2e_eric-bordeos.jpeg",
    "franchesca.jpeg": "672c7ddbf004d1237036cfa1_1675357551429.jpeg",
    "peter.jpg": "672a1b85b3cd4bc813cb85b5_63611faf1674a49cb0d8b8a3_peterg.jpg",
    "kurt.jpg": "672a1b8ec29b0c642b1a0662_63611fa15ea5085c9d3d958a_kurtivy-p-500.jpg",
    "pamela.png": "672a1bc3c80a4905d20227d8_63611ec117f6cec3567053e9_pamala.png",
    "paul.jpg": "672a1be9abbe013529770f03_63611cf9e1900528cd1a21b2_Paul-Beale-p-500.jpg",
    "jo-anne.png": "672a1bf0c29b0c642b1a764d_63611e9d2eed4163e6156661_joanne.png",
    "aaron.png": "672a1bb7fd769b51680d79ea_63611eeb13fa6e587735b1cc_aaron.png",
    "deryck.jpg": "672a1bfc950f1bfa84220222_63611cf0a4d7e732337e1197_deryk.jpg",
}

PHOTO_BY_NAME = {
    "Deryck": "/images/testimonials/deryck.jpg",
    "Dan Frickey": "/images/testimonials/dan-frickey.webp",
    "Randy Gray": "/images/testimonials/randy-gray.jpeg",
    "Ginger Chien": "/images/testimonials/ginger-chien.jpg",
    "Bo Ward": "/images/testimonials/bo-ward.jpg",
    "Eric Bordeos": "/images/testimonials/eric-bordeos.jpeg",
    "Franchesca": "/images/testimonials/franchesca.jpeg",
    "Peter": "/images/testimonials/peter.jpg",
    "Kurt": "/images/testimonials/kurt.jpg",
    "Pamela": "/images/testimonials/pamela.png",
    "Paul": "/images/testimonials/paul.jpg",
    "Maebel Reliquias": "/images/testimonials/maebel-reliquias.jpeg",
    "Jordan Carter": "/images/testimonials/jordan-carter.jpeg",
    "Jaeyoung Choi": "/images/testimonials/jae-choi.jpg",
    "Jo Anne": "/images/testimonials/jo-anne.png",
    "Aaron": "/images/testimonials/aaron.png",
    "Terri Wiksten": "/images/testimonials/terri-wiksten.webp",
    "Oscar Mendoza": "/images/testimonials/oscar-mendoza.jpg",
    "Emiliano Basso": "/images/testimonials/emiliano-basso.jpeg",
    "Mark Tanyag": "/images/testimonials/mark-tanyag.jpeg",
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, path in DOWNLOADS.items():
        dest = OUT / filename
        url = CDN + path
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, dest)

    data = json.loads((ROOT / "testimonials.json").read_text(encoding="utf-8"))
    for item in data:
        photo = PHOTO_BY_NAME.get(item["name"])
        if photo:
            item["photo"] = photo
    (ROOT / "testimonials.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("Updated testimonials.json")


if __name__ == "__main__":
    main()
