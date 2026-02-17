---
name: investment-advisor
description: Provides long-term investment guidance, portfolio allocation strategies, and financial planning for Turkish investors. Use when user says "yatırım tavsiyesi", "portföy oluştur", "investment advice", "portfolio allocation", "emeklilik planı", "uzun vadeli yatırım", "long-term investing".
license: MIT
metadata:
  version: 1.0.0
  author: its-meseba
  tags: [investment, portfolio, asset-allocation, turkish-markets, financial-planning, bist]
compatibility:
  models: [claude-3-5-sonnet, claude-3-opus]
  platforms: [claude-ai, claude-code, api]
allowed-tools:
  - web_search
  - calculator
  - file_operations
---

# Investment Advisor

## Overview

The Investment Advisor skill provides comprehensive long-term investment guidance, portfolio construction strategies, and financial planning tailored for Turkish investors. It covers asset allocation, Turkish investment instruments (BIST stocks, eurobonds, gold, government bonds), risk profiling, and retirement planning.

## Instructions

### Portfolio Construction Workflow

When a user requests investment advice or portfolio creation:

1. **Understand investor profile**
   - Investment goals (retirement, wealth building, education fund, etc.)
   - Time horizon (short-term <3 years, medium-term 3-10 years, long-term >10 years)
   - Risk tolerance (conservative, moderate, aggressive)
   - Current financial situation (income, savings, existing investments)
   - Age and life stage
   - Investment knowledge level

2. **Define asset allocation strategy**
   - Determine target allocation across asset classes
   - Consider Turkish-specific instruments and global diversification
   - Balance between TRY-denominated and hard currency assets
   - Factor in currency risk (USD/TRY, EUR/TRY)

3. **Recommend specific investment instruments**
   
   **Turkish Market Instruments**:
   - **BIST Stocks**: Blue-chip stocks (banking, holdings, industrials)
   - **Government Bonds (DİBS)**: TRY-denominated treasury bonds
   - **Eurobonds**: Hard currency Turkish government bonds
   - **Gold (Altın)**: Physical gold, gold ETFs, gold accounts
   - **Private Pension System (BES)**: Retirement funds
   - **Real Estate (Gayrimenkul)**: Direct property or REITs
   
   **Global Instruments** (if accessible):
   - International stocks (US, European markets)
   - Global bonds
   - International ETFs
   - Commodities

4. **Create diversified portfolio**
   - Allocate across instruments based on profile
   - Ensure adequate diversification (don't put all eggs in one basket)
   - Balance growth and income objectives
   - Consider tax implications (Turkish tax on capital gains, dividends)

5. **Establish rebalancing strategy**
   - Set rebalancing schedule (quarterly, semi-annual, annual)
   - Define rebalancing triggers (e.g., if allocation drifts >5%)
   - Plan for regular contributions (TRY cost averaging)

6. **Present the plan**
   - Clear allocation breakdown with percentages
   - Specific instrument recommendations
   - Expected returns and risks
   - Implementation steps
   - Monitoring and review schedule

### Risk Profiling

Assess investor risk tolerance through these dimensions:

**Financial Capacity**:
- Emergency fund adequate? (3-6 months expenses)
- Stable income?
- Debt levels manageable?
- Time horizon sufficient?

**Emotional Tolerance**:
- How would you react to a 20% portfolio decline?
- Can you stay invested during market downturns?
- Do you check portfolio daily or quarterly?

**Investment Knowledge**:
- Understanding of different asset classes
- Experience with market volatility
- Familiarity with Turkish markets

**Risk Profiles**:
- **Conservative**: Capital preservation, stable income, low volatility
  - Typical allocation: 70% bonds/fixed income, 20% gold, 10% stocks
- **Moderate**: Balanced growth and income, moderate volatility
  - Typical allocation: 50% stocks, 30% bonds, 10% gold, 10% alternatives
- **Aggressive**: High growth, accept high volatility
  - Typical allocation: 80% stocks, 15% alternatives, 5% bonds

### Turkish Investment Instruments Guide

**BIST Stocks (Hisse Senetleri)**:
- Blue-chip recommendations: Banks (GARAN, ISCTR, AKBNK), Holdings (KCHOL, SAHOL), Industrials (THYAO)
- Sector diversification: Banking, energy, telecommunications, consumer goods
- Consider dividend yields (many Turkish stocks pay dividends)
- Watch for foreign ownership limits

**Government Bonds (Devlet İç Borçlanma Senetleri - DİBS)**:
- Fixed income in TRY
- Various maturities (short-term, medium-term, long-term)
- Traded on BIST
- Consider inflation-indexed bonds (TÜFE'ye Endeksli)

**Eurobonds**:
- Turkish government bonds in USD or EUR
- Lower risk than TRY bonds in real terms
- Protects against TRY depreciation
- Typically longer maturities

**Gold (Altın)**:
- Hedge against currency depreciation
- Physical gold, gold accounts (Altın Hesabı), gold ETFs
- No yield but capital appreciation potential
- Cultural significance in Turkish saving culture

**Private Pension System (Bireysel Emeklilik Sistemi - BES)**:
- Government matching contribution (25% for first 3 years, then varies)
- Tax benefits
- Various fund options (stocks, bonds, mixed)
- Long-term commitment (10 years for full benefits)

## Examples

### Example 1: Young Professional Portfolio

**User Request**: "30 yaşındayım, yeni işe başladım, ilk yatırımımı yapmak istiyorum" (I'm 30, just started working, want to make my first investment)

**Investment Advisor Response**:
```
Genç Profesyonel Portföyü | Young Professional Portfolio
Profil / Profile: 30 yaş, uzun vadeli, agresif büyüme odaklı

📊 Önerilen Portföy Dağılımı / Recommended Allocation:

1. BIST Hisseleri / BIST Stocks (50%):
   - Bankacılık: GARAN, AKBNK (15%)
   - Holding: KCHOL, SAHOL (10%)
   - Teknoloji/Telekom: TTKOM, ASELS (15%)
   - Tüketim: BIMAS, ULKER (10%)

2. Altın / Gold (15%):
   - Fiziki altın veya altın hesabı
   - Physical gold or gold account
   - Enflasyon ve kur koruması

3. Eurobond (20%):
   - USD veya EUR cinsinden Türkiye tahvilleri
   - Kur riskinden korunma
   - Currency risk hedge

4. Uluslararası Hisseler / International Stocks (10%):
   - S&P 500 ETF (eğer erişim varsa)
   - Global diversification

5. Acil Fon / Emergency Fund (5%):
   - Likit, mevduat veya para piyasası fonu
   - Liquid, deposit or money market fund

💡 Strateji / Strategy:
- Aylık düzenli yatırım (maaşın %20'si)
- Monthly regular investment (20% of salary)
- 30 yıllık zaman ufku var, volatiliteyi kaldırabilir
- 30-year horizon, can handle volatility
- Her 6 ayda portföy dengele
- Rebalance every 6 months

🎯 Beklenen Getiri / Expected Return: %12-15 (uzun vadeli TRY bazında)
⚠️ Risk Seviyesi / Risk Level: Yüksek / High

📈 5 Yıl Sonrası Hedef / 5-Year Target:
- Portföy büyümesi + düzenli katkılar
- Portfolio growth + regular contributions
- Sonraki adım: Ev alımı için birikim
- Next step: Save for house purchase
```

### Example 2: Retirement Planning

**User Request**: "45 yaşındayım, emeklilik için portföy oluşturmak istiyorum" (I'm 45, want to create retirement portfolio)

**Investment Advisor Response**:
```
Emeklilik Portföyü | Retirement Portfolio
Profil / Profile: 45 yaş, 20 yıl vadeye kadar, moderate risk

📊 Portföy Dağılımı / Portfolio Allocation:

1. Bireysel Emeklilik Sistemi - BES (30%):
   - Hisse senedi ağırlıklı fon (%70 hisse)
   - Devlet katkısından yararlan (25%)
   - Stock-heavy fund, utilize state contribution

2. BIST Blue-Chip Hisseleri (25%):
   - Temettü veren hisseler odaklı
   - Dividend-paying focus
   - GARAN, THYAO, EREGL, KCHOL

3. Devlet Tahvilleri - DİBS (20%):
   - Sabit gelir bileşeni
   - Fixed income component
   - Enflasyona endeksli tahviller tercih et

4. Eurobond (15%):
   - Kur koruması
   - Currency hedge
   - 5-10 yıl vade

5. Altın (10%):
   - Güvenli liman
   - Safe haven
   - Fiziki veya hesap

💰 Aylık Katkı Önerisi / Monthly Contribution:
- Gelirin %25-30'u
- 25-30% of income
- TRY cost averaging stratejisi

🎯 Hedef / Goal:
- 65 yaşında rahat emeklilik
- Comfortable retirement at 65
- Aylık gelirin %70-80'i kadar emeklilik geliri
- Retirement income 70-80% of current income

📅 Gözden Geçirme / Review:
- Her yıl risk toleransını değerlendir
- Evaluate risk tolerance yearly
- 55 yaşından sonra daha muhafazakâr ağırlık
- Shift more conservative after 55
```

### Example 3: Asset Allocation Adjustment

**User Request**: "Portfolio allocation advice for moderate risk investor"

**Investment Advisor Response**:
```
Moderate Risk Portfolio Allocation

Profile: Balanced growth and income, moderate volatility tolerance

📊 Model Allocation:

Stocks (50%):
├── Turkish Stocks - BIST (30%)
│   ├── Large-cap blue chips (20%)
│   └── Mid-cap growth (10%)
└── International Stocks (20%)
    ├── US markets (S&P 500) (12%)
    └── European/Emerging (8%)

Fixed Income (30%):
├── Turkish Government Bonds (15%)
│   ├── Regular bonds (10%)
│   └── Inflation-indexed (5%)
└── Eurobonds (15%)
    └── USD/EUR denominated

Alternative Assets (15%):
├── Gold (10%)
│   └── Physical or ETF
└── REITs (5%)
    └── Turkish or international

Cash/Liquid (5%):
└── Emergency fund + opportunities

💡 Key Principles:
1. **Diversification**: Across asset classes, geographies, currencies
2. **Rebalancing**: Quarterly or when drift >5%
3. **Currency Balance**: ~40% in hard currencies (USD/EUR)
4. **Income Generation**: Dividends + bond interest
5. **Growth Potential**: 50% in growth assets (stocks)

📈 Expected Outcomes:
- Long-term return: 8-12% in TRY terms
- Volatility: Moderate (20-30% max drawdown)
- Income yield: 4-6% annually
- Inflation protection: Through stocks and gold

⚙️ Implementation:
1. Open necessary accounts (brokerage, gold account, pension)
2. Fund allocation over 3-6 months (dollar-cost averaging)
3. Set up automatic contributions
4. Review quarterly, rebalance semi-annually
```

## Best Practices

### Diversification Principles
- **Asset class diversification**: Stocks, bonds, gold, alternatives
- **Geographic diversification**: Turkish + international exposure
- **Currency diversification**: Balance TRY and hard currency assets
- **Sector diversification**: Don't concentrate in one sector
- **Time diversification**: Regular contributions (TRY cost averaging)

### Turkish Investor Considerations
- **Currency risk**: TRY volatility requires hard currency exposure
- **Inflation**: Turkish inflation high; need real return focus
- **Tax efficiency**: Know capital gains tax rules, dividend withholding
- **Access to international markets**: May need international broker
- **State incentives**: Use BES government matching contribution

### Long-Term Investing Mindset
- **Time in market > Timing market**: Stay invested through cycles
- **Emotion management**: Don't panic sell in downturns
- **Regular reviews**: Quarterly check, not daily obsession
- **Stay the course**: Trust your plan during volatility
- **Adjust as needed**: Life changes may require allocation changes

### Risk Management
- **Emergency fund first**: 3-6 months expenses in liquid assets
- **Avoid debt for investing**: Pay off high-interest debt first
- **Don't invest money you need soon**: Match horizon to goals
- **Understand what you own**: Only invest in instruments you understand
- **Regular rebalancing**: Maintains risk level, forces buy-low-sell-high

## Troubleshooting

### Issue: Portfolio declining in value

**Solution**: 
- Is this temporary market volatility or fundamental change?
- Review if allocation still matches your goals and risk tolerance
- If long-term plan unchanged, stay invested (don't panic sell)
- If fundamentals changed, reassess and adjust
- Consider this opportunity to rebalance or add at lower prices

### Issue: Currency depreciation affecting TRY returns

**Solution**:
- This is why hard currency exposure (eurobonds, international stocks, gold) is crucial
- Increase hard currency allocation if TRY outlook weak
- Gold acts as hedge against TRY depreciation
- Consider international assets if accessible

### Issue: Unclear which instruments to choose

**Solution**:
- Start with index funds or blue-chip stocks (diversification built-in)
- For bonds, use government bonds (lower risk than corporate)
- For gold, physical or bank gold accounts (simple and secure)
- Avoid complex derivatives or instruments you don't understand
- Consider BES funds (professional management)

### Issue: Can't afford recommended allocation

**Solution**:
- Start with what you can afford
- Focus on building emergency fund first
- Then begin with most important asset class for your profile
- Gradually add other assets as savings grow
- Even small regular contributions compound over time

## Financial Planning Framework

### Goal-Based Investing

**Short-term goals (<3 years)**:
- Examples: Emergency fund, vacation, car purchase
- Instruments: Deposits, money market, short-term bonds
- Priority: Capital preservation, liquidity

**Medium-term goals (3-10 years)**:
- Examples: House down payment, education fund
- Instruments: Balanced portfolio (stocks, bonds, gold)
- Priority: Moderate growth, controlled risk

**Long-term goals (>10 years)**:
- Examples: Retirement, wealth building
- Instruments: Stock-heavy portfolio, some alternatives
- Priority: Growth, can tolerate volatility

### Lifecycle Investing

**20s-30s**: Aggressive growth
- 70-80% stocks, minimal fixed income
- Long time to recover from downturns
- Build wealth foundation

**40s-50s**: Balanced approach
- 50-60% stocks, increasing fixed income
- Peak earning years
- Balance growth and stability

**60s+**: Capital preservation
- 30-40% stocks, majority in fixed income
- Need stable income
- Reduce volatility

## Notes

**Disclaimer**: This skill provides educational guidance and investment concepts. It is NOT personalized financial advice. Always consult with licensed financial advisors and tax professionals. Consider your personal circumstances, goals, and risk tolerance. Past performance doesn't guarantee future results.

**Turkish Regulations**: Investment regulations and tax rules in Turkey can change. Stay informed about current rules, especially regarding capital gains tax, dividend withholding, and foreign investment restrictions.

**Currency Considerations**: Turkish Lira (TRY) can be volatile. Hard currency exposure (eurobonds, international assets, gold) is often important for Turkish investors to preserve purchasing power.

**Continuous Learning**: Investment markets evolve. Stay informed about Turkish economic developments, TCMB (Central Bank) policies, and global market trends.
