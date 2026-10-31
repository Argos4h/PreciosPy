const fs = require('fs');
const path = require('path');

const files = [
  path.resolve(__dirname, '../precios_py_demo.html'),
  path.resolve('C:/Users/munic/.gemini/antigravity/brain/3ac93072-98c3-495f-ad02-c8cfc7984916/precios_py_interactive_demo.html')
];

files.forEach(f => {
  if (!fs.existsSync(f)) {
    console.error('File not found:', f);
    return;
  }
  let content = fs.readFileSync(f, 'utf8');

  // 1. Un-hardcode Tuesday active in Search tab
  content = content.replace(
    '<button onclick="setWeekday(2)" class="day-chip px-2.5 py-1 rounded-xl font-medium bg-emerald-500 text-white font-bold" data-day="2">Mar</button>',
    '<button onclick="setWeekday(2)" class="day-chip px-2.5 py-1 rounded-xl font-medium bg-[#1E293B] text-slate-400 hover:text-white border border-[#334155]" data-day="2">Mar</button>'
  );

  // 2. Un-hardcode Tuesday active in Promos tab
  content = content.replace(
    '<button onclick="setPromoDay(2)" class="promo-day-chip shrink-0 px-3 py-1 rounded-xl font-bold bg-emerald-500 text-white whitespace-nowrap" data-day="2">Mar</button>',
    '<button onclick="setPromoDay(2)" class="promo-day-chip shrink-0 px-3 py-1 rounded-xl font-medium bg-[#1E293B] text-slate-400 hover:text-white border border-[#334155] whitespace-nowrap" data-day="2">Mar</button>'
  );

  // 3. Dynamic today ISO day variable initialization
  const r3 = `    let isDarkMode = true;
    // Detección automática del día actual de la semana (1=Lunes ... 6=Sábado, 7=Domingo)
    function getTodayIsoDay() {
      const jsDay = new Date().getDay(); // 0: Dom, 1: Lun, ..., 6: Sáb
      return jsDay === 0 ? 7 : jsDay;
    }
    const dayShortNames = { 1: 'Lun', 2: 'Mar', 3: 'Mié', 4: 'Jue', 5: 'Vie', 6: 'Sáb', 7: 'Dom' };
    let selectedDay = getTodayIsoDay(); // Se auto-selecciona el día de hoy (Sábado = 6)
    let promoSelectedDay = getTodayIsoDay();`;

  content = content.replace(
    /let isDarkMode = true;\r?\n\s*let selectedDay = 2; \/\/ Martes por defecto \(Itaú en Superseis\)\r?\n\s*let promoSelectedDay = 2; \/\/ Día en pestaña Promos/,
    r3
  );

  // 4. Update day chip labels helper
  if (!content.includes('function updateDayChipLabels()')) {
    const fnUpdate = `    function updateDayChipLabels() {
      const today = getTodayIsoDay();
      document.querySelectorAll('.day-chip').forEach(c => {
        const d = parseInt(c.getAttribute('data-day'));
        const base = dayShortNames[d] || '';
        c.innerText = (d === today) ? \`\${base} • Hoy\` : base;
      });
      document.querySelectorAll('.promo-day-chip').forEach(c => {
        const d = parseInt(c.getAttribute('data-day'));
        const base = dayShortNames[d] || '';
        c.innerText = (d === today) ? \`\${base} • Hoy\` : base;
      });
    }

    function filterCategory(cat) {`;
    content = content.replace('    function filterCategory(cat) {', fnUpdate);
  }

  // 5. In renderPromosView: indicate Hoy in subtitle
  const t5 = "if (sub) sub.innerText = `${dayFullNames[promoSelectedDay]} • ${filtered.length} promociones vigentes`;";
  const r5 = `const isToday = promoSelectedDay === getTodayIsoDay();
      const dayLabel = isToday ? \`\${dayFullNames[promoSelectedDay]} (Hoy)\` : dayFullNames[promoSelectedDay];
      if (sub) sub.innerText = \`\${dayLabel} • \${filtered.length} promociones vigentes\`;`;
  content = content.replace(t5, r5);

  // 6. In DOMContentLoaded: call updateDayChipLabels, setWeekday and setPromoDay
  const t6 = /window\.addEventListener\('DOMContentLoaded', \(\) => \{\r?\n\s*applyTheme\(\);\r?\n\s*\}\);/;
  const r6 = `window.addEventListener('DOMContentLoaded', () => {
      applyTheme();
      updateDayChipLabels();
      setWeekday(selectedDay);
      setPromoDay(promoSelectedDay);
    });`;
  content = content.replace(t6, r6);

  fs.writeFileSync(f, content, 'utf8');
  console.log('Successfully updated:', f);
});

