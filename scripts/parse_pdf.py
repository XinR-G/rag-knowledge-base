from pathlib import Path
import time

from unstructured.partition.pdf import partition_pdf

RAW_DIR = Path("data/raw_pdfs")
OUT_DIR = Path("data/parsed")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def parse_one(pdf_path: Path) -> None:
    print(f"\n=== 解析: {pdf_path.name} ===")
    start = time.time()

    elements = partition_pdf(filename=str(pdf_path))

    elapsed = time.time() - start

    # 统计元素类型
    type_count = {}
    for el in elements:
        t = el.category
        type_count[t] = type_count.get(t, 0) + 1

    # 保存为纯文本
    out_txt = OUT_DIR / (pdf_path.stem + ".txt")
    with open(out_txt, "w", encoding="utf-8") as f:
        for el in elements:
            f.write(str(el) + "\n\n")

    # 打印统计
    print(f"耗时: {elapsed:.2f} 秒")
    print(f"元素总数: {len(elements)}")
    print("元素类型统计:")
    for t, c in sorted(type_count.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")
    print(f"已保存: {out_txt}")


if __name__ == "__main__":
    pdfs = sorted(RAW_DIR.glob("*.pdf"))
    if not pdfs:
        print(f"没有在 {RAW_DIR} 找到 PDF")
        raise SystemExit(1)

    for pdf in pdfs:
        parse_one(pdf)