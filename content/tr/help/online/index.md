---
title: "Cevrimici Yardim"
summary: "ForgeIEC editorunden baglamsal yardim icin giris noktasi"
---

## Cevrimici Yardim — Nedir?

Cevrimici yardim, ForgeIEC editorunun baglamsal yardim katmanidir.
Editorde **F1** tusuna basildiginda tarayiciniz su anda odaklanan
ogenin (dialog, panel, degisken tablosu, kod uretme eylemi ...) yardim
sayfasinda dogrudan acilir.

## URL semasi

Tum yardim sayfalari tek tip bir sema altinda yer alir:

```
https://forgeiec.io/<dil>/help/<konu>/
```

- `<dil>` editor yereline uyar (de, en, fr, es, ja, tr, zh, ar);
  yerel sayfa yoksa varsayilan olarak `de`
- `<konu>` tum dillerde ayni olan ve cevrilmeyen bir slug'tir

Boylece editoru baslatmadan bir yardim sayfasini dogrudan tarayicida
acabilirsiniz.

## Mevcut konular

### Editor ve diller

- [Structured Text (ST)](/tr/help/st/) — ST editoru ve dil temelleri
- [Instruction List (IL)](/tr/help/il/) — akumulator tabanli IEC dili
- [Function Block Diagram (FBD)](/tr/help/fbd/) — fonksiyon ve fonksiyon bloklarinin grafiksel baglantisi
- [Ladder Diagram (LD)](/tr/help/ld/) — elektrik semasi metaforu: guc raylari, kontaklar, bobinler
- [Sequential Function Chart (SFC)](/tr/help/sfc/) — sira kontrolu icin adim-gecis modeli

### Model ve degiskenler

- [Degisken yonetimi](/tr/help/variables/) — Variables paneli FAddressPool'a merkezi bakis
- [Kutuphane](/tr/help/library/) — IEC 61131-3 standart kutuphanesi + ForgeIEC uzantilari + kullanici tanimli bloklar
- [Ozellikler paneli](/tr/help/properties-panel/) — secili bus eleman icin inline editor
- [Tercihler](/tr/help/preferences/) — merkezi yapilandirma diyalogu: editor, runtime, PLC, AI asistani

### Bus ve donanim

- [Bus yapilandirmasi](/tr/help/bus-config/) — endustriyel saha bus yapilandirmasi icin PLCopen XML semasi

### Genel

- [Test kapsami](/tr/help/tests/) — IEC dil ozellik seti, standart bloklar ve multi-tasking icin 117 otomatik test
- [Acik kaynak felsefesi](/tr/help/open-source/) — arka plan

## Editorde

- **F1** odaklanan bir ogede → baglamsal yardim sayfasi
- **Yardim → Cevrimici Yardim** ana menude → giris noktasi (bu sayfa)
- **Yardim → ForgeIEC Hakkinda** → surum bilgisi + lisans
