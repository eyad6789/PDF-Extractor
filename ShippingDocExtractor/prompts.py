"""
Extraction prompts for Arabic shipping documents
"""

EXTRACTION_PROMPT = '''Analyze this Arabic shipping document PDF and extract the following data.
Return ONLY valid JSON in this exact format:

{
    "date": "the date from امر التسليم (delivery order date - تاريخ تنظيم امر تسليم)",
    "total_containers": number of containers,
    "bill_number": "رقم البوليصة (Bill of Lading number)",
    "description": "وصف البضاعة (product description)",
    "iraqi_bank_name": "Iraqi bank name from البيان الجمركي - look for اسم البنك. If no Iraqi bank, return null",
    "unit_price": unit price number,
    "currency": "USD or other",
    "has_customs_declaration": true or false (is there بيان جمركي page?),
    "has_bank": true or false (is there an Iraqi bank in the بيان?),
    "containers": [
        {
            "number": "container number",
            "weight": weight in kg as number
        }
    ]
}

EXTRACTION RULES:

1. DATE (التاريخ):
   - Find in Page 1 (امر التسليم)
   - Look for: تاريخ تنظيم امر تسليم
   - Format: YYYY/MM/DD

2. CONTAINER NUMBER (رقم الحاوية):
   - Find in Page 1 table
   - Examples: CAIU8827065, MSBU8337264, MSCU5176370
   - List ALL containers

3. TOTAL CONTAINERS (عدد الحاويات):
   - Count how many containers in the shipment

4. BILL NUMBER (رقم البوليصة):
   - Find in Page 1 or Page 2
   - Example: MEDUYX748666

5. PRODUCT DESCRIPTION (وصف البضاعة):
   - Find in Page 1 table or Page 2
   - Example: CHAIR, CHAIR, WORDPAD

6. WEIGHT (الوزن):
   - Find weight for EACH container
   - In KG (كغ)

7. IRAQI BANK (البنك العراقي):
   - Find in البيان الجمركي (customs declaration page)
   - Look for Iraqi bank names like:
     * مصرف الرافدين
     * مصرف الرشيد  
     * المصرف التجاري العراقي
     * مصرف الشرق الأوسط
   - If NO Iraqi bank found → return null
   - Do NOT confuse with:
     * Vessel name (MSC FAITH)
     * Chinese ports (Tianjin, Xingang)
     * Shipping company names

8. UNIT PRICE (سعر الوحدة):
   - Find in البيان الجمركي
   - Usually in USD

9. HAS بيان (يوجد بيان):
   - Check if there is a بيان جمركي page
   - true = yes, false = no

Return ONLY the JSON, no markdown, no explanation.'''

# Excel column mapping (Arabic headers)
EXCEL_COLUMNS = {
    "date": "التاريخ",
    "container_number": "رقم الحاوية",
    "total_containers": "عدد الحاويات",
    "bill_number": "رقم البوليصة",
    "description": "وصف البضاعة",
    "weight": "الوزن",
    "iraqi_bank_name": "البنك العراقي",
    "unit_price": "سعر الوحدة",
    "has_customs_declaration": "يوجد بيان"
}
