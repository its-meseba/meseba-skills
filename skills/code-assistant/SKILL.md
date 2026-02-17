---
name: code-assistant
description: Helps write, review, debug, and optimize code across multiple languages with Turkish developer conventions. Use when user says "kod yaz", "debug et", "code review", "write code", "hata bul", "optimize et", "kod incele", "refactor".
license: MIT
metadata:
  version: 1.0.0
  author: its-meseba
  tags: [coding, debugging, code-review, optimization, turkish-developers, refactoring]
compatibility:
  models: [claude-3-5-sonnet, claude-3-opus]
  platforms: [claude-ai, claude-code, api]
allowed-tools:
  - file_operations
  - bash
  - web_search
---

# Code Assistant

## Overview

The Code Assistant helps developers write, review, debug, and optimize code across multiple programming languages. It supports Turkish developer conventions and bilingual communication, making it perfect for Turkish developers who work with international codebases.

## Instructions

### Code Generation Workflow

When a user requests code to be written:

1. **Understand requirements**
   - What functionality is needed?
   - Which programming language(s)?
   - Any specific frameworks or libraries?
   - Code style preferences (Turkish comments? English comments?)
   - Target environment (web, mobile, backend, etc.)

2. **Design approach**
   - Identify the best solution pattern
   - Consider edge cases and error handling
   - Plan for maintainability and scalability
   - Choose appropriate data structures and algorithms

3. **Write clean code**
   - Follow language-specific best practices
   - Use clear, descriptive naming (English or Turkish as requested)
   - Add appropriate comments (bilingual if helpful)
   - Include error handling and validation
   - Consider performance implications

4. **Provide context**
   - Explain the code logic
   - Highlight important design decisions
   - Note any dependencies or requirements
   - Suggest testing approaches

### Code Review Workflow

When a user requests code review:

1. **Understand the code**
   - Read and comprehend the code logic
   - Identify the code's purpose and context
   - Note the language, frameworks, and patterns used

2. **Evaluate code quality**
   - **Correctness**: Does it work as intended?
   - **Readability**: Is it easy to understand?
   - **Maintainability**: Can it be easily modified?
   - **Performance**: Are there efficiency concerns?
   - **Security**: Are there vulnerabilities?
   - **Best practices**: Does it follow language conventions?

3. **Identify issues**
   - Bugs or logic errors
   - Code smells (duplicated code, long functions, etc.)
   - Security vulnerabilities
   - Performance bottlenecks
   - Style inconsistencies
   - Missing error handling

4. **Provide feedback**
   - Categorize issues by severity (Critical, Major, Minor, Suggestion)
   - Explain WHY something is an issue
   - Suggest specific improvements with examples
   - Highlight what's done well (positive feedback)
   - Prioritize recommendations

### Debugging Workflow

When a user needs help debugging:

1. **Gather information**
   - What's the error message or unexpected behavior?
   - Which code is causing the issue?
   - What's the expected vs. actual behavior?
   - Steps to reproduce the issue
   - Environment details (language version, OS, etc.)

2. **Analyze the problem**
   - Review relevant code sections
   - Trace the execution flow
   - Identify potential causes
   - Check for common pitfalls

3. **Formulate hypothesis**
   - Propose likely causes based on analysis
   - Explain the reasoning
   - Consider edge cases

4. **Suggest solutions**
   - Provide specific fixes with code examples
   - Explain why the fix works
   - Suggest preventive measures
   - Recommend debugging techniques for similar issues

### Code Optimization Workflow

When a user requests optimization:

1. **Measure current state**
   - Identify performance bottlenecks
   - Check time complexity
   - Analyze space usage
   - Profile if possible

2. **Identify optimization opportunities**
   - Algorithm improvements
   - Data structure changes
   - Caching strategies
   - Database query optimization
   - Async/parallel processing opportunities

3. **Apply optimizations**
   - Implement improvements
   - Maintain code readability
   - Ensure correctness is preserved
   - Add comments explaining optimization

4. **Validate improvements**
   - Estimate performance gains
   - Suggest benchmarking approaches
   - Note any trade-offs

## Examples

### Example 1: Code Generation (Turkish Request)

**User Request**: "Python'da bir liste içindeki tekrar eden elemanları bulan fonksiyon yaz" (Write a Python function to find duplicate elements in a list)

**Code Assistant Response**:
```python
def tekrar_edenleri_bul(liste):
    """
    Bir liste içindeki tekrar eden elemanları bulur ve döndürür.
    Finds and returns duplicate elements in a list.
    
    Args:
        liste: İncelenecek liste / List to check
    
    Returns:
        Tekrar eden elemanların listesi / List of duplicate elements
    """
    gorulmus = set()
    tekrarlar = set()
    
    for eleman in liste:
        if eleman in gorulmus:
            tekrarlar.add(eleman)
        else:
            gorulmus.add(eleman)
    
    return list(tekrarlar)

# Kullanım örneği / Usage example
sayilar = [1, 2, 3, 2, 4, 5, 1, 6, 7, 5]
tekrar_edenler = tekrar_edenleri_bul(sayilar)
print(f"Tekrar eden sayılar: {tekrar_edenler}")
# Çıktı / Output: Tekrar eden sayılar: [1, 2, 5]
```

**Açıklama / Explanation**:
- `set()` kullanarak O(1) arama karmaşıklığı sağladık
- Used `set()` for O(1) lookup complexity
- İki set: biri tüm görülenleri, diğeri tekrarları tutuyor
- Two sets: one for all seen items, one for duplicates
- Fonksiyon okunabilir Türkçe değişken isimleri kullanıyor
- Function uses readable Turkish variable names

### Example 2: Code Review

**User Request**: "Review this JavaScript code"

```javascript
function calculateTotal(items) {
  var total = 0;
  for (var i = 0; i < items.length; i++) {
    total = total + items[i].price * items[i].quantity;
  }
  return total;
}
```

**Code Assistant Response**:
```
Code Review - calculateTotal Function

✅ Strengths (İyi Yanlar):
- Simple and clear logic
- Correctly calculates total

⚠️ Issues & Suggestions (Sorunlar & Öneriler):

1. [Minor] Use 'const' instead of 'var'
   Neden / Why: var has function scope, const/let have block scope
   
   Öneri / Suggestion:
   ```javascript
   function calculateTotal(items) {
     let total = 0;
     for (let i = 0; i < items.length; i++) {
       total += items[i].price * items[i].quantity;
     }
     return total;
   }
   ```

2. [Suggestion] Use modern array methods
   Neden / Why: More readable, functional style
   
   Öneri / Suggestion:
   ```javascript
   function calculateTotal(items) {
     return items.reduce((total, item) => {
       return total + (item.price * item.quantity);
     }, 0);
   }
   ```

3. [Major] Missing input validation
   Neden / Why: Function will crash if items is null/undefined
   
   Öneri / Suggestion:
   ```javascript
   function calculateTotal(items) {
     if (!items || !Array.isArray(items)) {
       return 0; // or throw error
     }
     
     return items.reduce((total, item) => {
       // Also validate item properties
       const price = item.price || 0;
       const quantity = item.quantity || 0;
       return total + (price * quantity);
     }, 0);
   }
   ```

4. [Suggestion] Add JSDoc comments
   ```javascript
   /**
    * Calculates the total price of all items
    * Tüm ürünlerin toplam fiyatını hesaplar
    * 
    * @param {Array<{price: number, quantity: number}>} items - Array of items
    * @returns {number} Total price
    */
   function calculateTotal(items) {
     // ... implementation
   }
   ```

🎯 Priority Actions:
1. Add input validation (Major)
2. Use const/let instead of var (Minor)
3. Consider modern array methods for readability (Optional)
```

### Example 3: Debugging

**User Request**: "Kod hata veriyor: 'TypeError: Cannot read property 'length' of undefined'" (Code gives error)

**Code Assistant Response**:
```
Hata Analizi / Error Analysis

❌ Hata / Error: TypeError: Cannot read property 'length' of undefined

🔍 Neden / Cause:
'length' özelliğine erişmeye çalıştığınız değişken undefined
You're trying to access 'length' property on an undefined variable

💡 Olası Senaryolar / Possible Scenarios:

1. Değişken hiç tanımlanmamış / Variable not initialized
   ```javascript
   let myArray; // undefined
   console.log(myArray.length); // ❌ Hata!
   ```

2. Fonksiyon parametre almamış / Function didn't receive parameter
   ```javascript
   function process(data) {
     return data.length; // data undefined ise hata
   }
   process(); // ❌ parametre verilmemiş
   ```

3. API'den veri gelmemiş / Data not returned from API
   ```javascript
   const response = await fetchData();
   console.log(response.items.length); 
   // response.items undefined ise hata
   ```

🔧 Çözümler / Solutions:

1. **Default değer kullan / Use default value:**
   ```javascript
   function process(data = []) {
     return data.length; // ✅ data undefined ise [] kullanılır
   }
   ```

2. **Kontrol ekle / Add check:**
   ```javascript
   function process(data) {
     if (!data) {
       console.error('Data is undefined');
       return 0;
     }
     return data.length;
   }
   ```

3. **Optional chaining kullan / Use optional chaining (ES2020+):**
   ```javascript
   const length = myArray?.length ?? 0;
   // myArray undefined ise 0 döner
   ```

4. **Nullish coalescing ile birlikte / With nullish coalescing:**
   ```javascript
   const response = await fetchData();
   const items = response?.items ?? [];
   console.log(items.length); // ✅ Güvenli
   ```

📝 Debug Stratejisi / Debug Strategy:
1. Hatanın tam satırını bul / Find exact line with error
2. console.log ile değişkeni kontrol et / Check variable with console.log
3. Değişkenin nereden geldiğini takip et / Trace where variable comes from
4. Uygun çözümü uygula / Apply appropriate solution
```

### Example 4: Optimization

**User Request**: "Optimize this slow code"

```python
def find_duplicates(list1, list2):
    duplicates = []
    for item1 in list1:
        for item2 in list2:
            if item1 == item2:
                duplicates.append(item1)
    return duplicates
```

**Code Assistant Response**:
```
Optimizasyon Analizi / Optimization Analysis

📊 Mevcut Durum / Current State:
- Zaman Karmaşıklığı / Time Complexity: O(n*m)
- Alan Karmaşıklığı / Space Complexity: O(k) where k is duplicates
- Problem: Nested loops causing slow performance

⚡ Optimize Edilmiş Kod / Optimized Code:

```python
def find_duplicates(list1, list2):
    """
    İki liste arasındaki ortak elemanları bulur (optimize edilmiş).
    Finds common elements between two lists (optimized).
    
    Zaman Karmaşıklığı / Time Complexity: O(n + m)
    Alan Karmaşıklığı / Space Complexity: O(n + k)
    """
    set1 = set(list1)  # O(n) zaman, O(n) alan
    duplicates = [item for item in list2 if item in set1]  # O(m) zaman
    return duplicates

# Alternatif: Set intersection kullan / Use set intersection
def find_duplicates_alt(list1, list2):
    """Daha kısa ama sonuç set olarak döner."""
    return list(set(list1) & set(list2))
```

📈 Performans Kazancı / Performance Gain:
- Eski / Old: O(n*m) → 10,000 x 10,000 = 100M operations
- Yeni / New: O(n + m) → 10,000 + 10,000 = 20K operations
- İyileşme / Improvement: ~5000x faster for large lists!

💡 Açıklama / Explanation:
1. list1'i set'e dönüştürüyoruz (O(n))
   Converting list1 to set takes O(n)

2. set'te arama O(1), liste yerine O(m)
   Lookup in set is O(1), instead of O(m) in list

3. Tek döngü yeterli, nested loop yok
   Single loop sufficient, no nested loop

⚖️ Trade-offs:
- Daha fazla bellek kullanır (set için)
  Uses more memory (for the set)
- Çok küçük listeler için (<100 eleman) fark az
  For very small lists (<100 items), difference minimal
- Sıralama korunmaz (önemliyse sorted() kullan)
  Order not preserved (use sorted() if needed)

🎯 Kullanım / Usage:
```python
# Test
list1 = list(range(10000))
list2 = list(range(5000, 15000))

import time
start = time.time()
result = find_duplicates(list1, list2)
end = time.time()
print(f"Süre / Time: {end - start:.4f} seconds")
print(f"Ortak eleman sayısı / Common elements: {len(result)}")
```
```

## Best Practices

### Code Quality Principles
- **Readability**: Code is read more than written
- **DRY**: Don't Repeat Yourself
- **KISS**: Keep It Simple, Stupid
- **YAGNI**: You Aren't Gonna Need It
- **SOLID**: Single responsibility, Open-closed, Liskov substitution, Interface segregation, Dependency inversion

### Turkish Developer Conventions
- **Variable naming**: Can use Turkish or English, be consistent
- **Comments**: Bilingual comments helpful for international teams
- **Documentation**: English for public APIs, Turkish acceptable for internal
- **Error messages**: Consider bilingual error messages for user-facing apps

### Language-Specific Best Practices
- **Python**: Follow PEP 8, use type hints
- **JavaScript**: Use modern ES6+, proper async/await
- **Java**: Follow naming conventions, use proper access modifiers
- **C#**: Follow Microsoft conventions, use LINQ appropriately
- **Go**: Follow Go conventions, proper error handling

### Security Considerations
- **Input validation**: Always validate user input
- **SQL injection**: Use parameterized queries
- **XSS**: Sanitize output in web apps
- **Authentication**: Use established libraries, don't roll your own
- **Secrets**: Never hardcode credentials

## Troubleshooting

### Issue: Code works locally but fails in production

**Solution**:
- Check environment differences (Node version, dependencies, env variables)
- Review logs for specific error messages
- Verify all configuration is properly set
- Check for hardcoded paths or assumptions
- Test with production-like data

### Issue: Performance issue not clear where

**Solution**:
- Use profiling tools (Python: cProfile, JS: Chrome DevTools)
- Add timing logs at key points
- Check database query performance (use EXPLAIN)
- Review algorithm complexity
- Check for memory leaks

### Issue: Can't understand legacy code

**Solution**:
- Start with high-level overview (what does it do?)
- Trace execution flow with debugger
- Add comments as you understand sections
- Look for entry points and follow from there
- Refactor small sections incrementally

### Issue: Unsure which approach to use

**Solution**:
- Consider trade-offs (performance, readability, maintainability)
- Check existing codebase patterns
- Prototype both approaches if time permits
- Consult language/framework best practices
- When in doubt, choose simplicity

## Notes

**Language Support**: This skill supports multiple programming languages including Python, JavaScript/TypeScript, Java, C#, Go, Ruby, PHP, and more. Specify your language for best results.

**Bilingual Support**: The skill can communicate in both Turkish and English, and can handle code with Turkish variable names, comments, or documentation.

**Code Style**: By default, follows language-specific best practices. Specify if you have particular style preferences (e.g., "Turkish variable names", "English comments only").

**Tool Integration**: Works well with IDEs, version control systems, and can provide commands for linters, formatters, and testing frameworks.
