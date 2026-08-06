const curatedDeals = [
  {
    id: 1,
    date: "July 16, 2026",
    acquirer: "ABB",
    target: "Rotork",
    headline: "ABB agrees to acquire Rotork",
    valueBillions: 5.5,
    sector: "Industrial technology",
    countries: ["Switzerland", "United Kingdom"],
    status: "Announced",
    crossBorder: true,
    summary: "ABB’s largest acquisition expands its automation and electrification portfolio through Rotork’s flow-control products.",
    intent: "Add a high-margin industrial automation platform and deepen exposure to electrification, process automation, and data-center demand.",
    longTermGoals: ["Expand automation capabilities", "Add recurring aftermarket revenue", "Strengthen presence in process industries"],
    culture: "Moderate integration risk: both are engineering-led industrial businesses, but ABB is much larger and more globally matrixed.",
    geography: "Cross-border European transaction with manageable distance, but multiple regulatory and operational jurisdictions.",
    valuation: "Approximately $5.5 billion, with a large premium that puts pressure on ABB to deliver synergies and growth.",
    shareholderValue: "Rotork shareholders benefit from the premium. ABB investors may focus on execution risk, purchase price, and returns on invested capital.",
    scores: { strategic: 9, cultural: 7, geographic: 8, valuation: 6 },
    source: "https://www.reuters.com/business/abb-beats-forecasts-with-q2-earnings-announces-biggest-ever-acquisition-2026-07-16/"
  },
  {
    id: 2,
    date: "July 17, 2026",
    acquirer: "PIF-led consortium",
    target: "Electronic Arts",
    headline: "PIF-led consortium advances EA acquisition",
    valueBillions: 55,
    sector: "Gaming",
    countries: ["Saudi Arabia", "United States"],
    status: "Pending review",
    crossBorder: true,
    summary: "A consortium led by Saudi Arabia’s Public Investment Fund is pursuing a large leveraged acquisition of Electronic Arts.",
    intent: "Build a global gaming platform and support Saudi Arabia’s strategy of diversifying beyond oil into entertainment and technology.",
    longTermGoals: ["Scale global gaming exposure", "Diversify national investment portfolio", "Own durable entertainment intellectual property"],
    culture: "High complexity: a public U.S. creative company would operate under ownership involving a sovereign wealth fund and private investors.",
    geography: "Significant distance, regulatory review, and potential political scrutiny across the U.S., Saudi Arabia, and Europe.",
    valuation: "Approximately $55 billion and heavily financed, making debt service, cash-flow durability, and franchise performance central concerns.",
    shareholderValue: "EA shareholders receive a takeover premium. Consortium returns depend on long-term cash generation, game pipeline strength, and financing costs.",
    scores: { strategic: 8, cultural: 5, geographic: 4, valuation: 5 },
    source: "https://www.reuters.com/business/saudi-pif-set-win-eu-nod-electronic-arts-deal-under-subsidy-rules-sources-say-2026-07-17/"
  },
  {
    id: 3,
    date: "July 13, 2026",
    acquirer: "Aditya Birla Renewables",
    target: "Sprng Energy",
    headline: "Aditya Birla Renewables to buy Sprng Energy",
    valueBillions: 1.8,
    sector: "Renewable energy",
    countries: ["India", "United Kingdom"],
    status: "Announced",
    crossBorder: true,
    summary: "The transaction adds substantial renewable generation capacity and accelerates Aditya Birla’s position in India’s clean-energy market.",
    intent: "Scale renewable capacity quickly rather than building the entire portfolio organically, while Shell narrows its strategic focus.",
    longTermGoals: ["Increase renewable capacity", "Compete at national scale", "Support India’s energy-transition demand"],
    culture: "Moderate risk because the acquired operating platform is India-focused, although ownership is transferring from a global energy major.",
    geography: "Operations are primarily in India, reducing day-to-day distance after closing despite the cross-border seller relationship.",
    valuation: "$1.8 billion including debt; the key question is whether future power revenues justify the purchase and financing mix.",
    shareholderValue: "Potential value comes from scale and growth, while investors will watch leverage, project execution, and power-market economics.",
    scores: { strategic: 9, cultural: 7, geographic: 8, valuation: 7 },
    source: "https://www.reuters.com/business/energy/indias-aditya-birla-groups-renewables-arm-buy-sprng-energy-shell-2026-07-13/"
  },
  {
    id: 4,
    date: "July 17, 2026",
    acquirer: "EQT / rival consortium",
    target: "Kakaku.com",
    headline: "Bidding contest intensifies for Kakaku.com",
    valueBillions: 4.2,
    sector: "Internet services",
    countries: ["Sweden", "Japan"],
    status: "Competitive bid",
    crossBorder: true,
    summary: "EQT raised its offer for Japanese website operator Kakaku.com, competing with a rival group involving LY Corp and Bain Capital.",
    intent: "Gain control of established Japanese digital marketplaces and their recurring consumer traffic, data, and advertising economics.",
    longTermGoals: ["Acquire scaled digital platforms", "Improve monetization", "Capture operational upside through private ownership"],
    culture: "High integration sensitivity because Japanese governance and stakeholder practices can differ from Western private-equity operating models.",
    geography: "Cross-border ownership and local-market execution increase complexity, though the target remains operationally concentrated in Japan.",
    valuation: "About $4.2 billion at the revised offer; a bidding war can increase the risk of overpayment.",
    shareholderValue: "Target shareholders may benefit from competing bids. Buyer returns become harder to achieve as the purchase price rises.",
    scores: { strategic: 8, cultural: 5, geographic: 5, valuation: 4 },
    source: "https://www.reuters.com/world/asia-pacific/eqt-raises-kakakucom-offer-price-3450-yen-topping-rival-bid-2026-07-17/"
  }
];

const generatedDeals = Array.isArray(window.generatedDeals) ? window.generatedDeals : [];
const deals = [...generatedDeals, ...curatedDeals];

const outlets = [
  { name: "Bloomberg", url: "https://www.bloomberg.com/", note: "Markets, companies, and deal reporting" },
  { name: "Reuters", url: "https://www.reuters.com/", note: "Fast global transaction reporting" },
  { name: "The Wall Street Journal", url: "https://www.wsj.com/", note: "Corporate and market analysis" },
  { name: "Financial Times", url: "https://www.ft.com/", note: "Global business and cross-border deals" },
  { name: "CNBC", url: "https://www.cnbc.com/", note: "Market reaction and executive interviews" },
  { name: "GuruFocus", url: "https://www.gurufocus.com/", note: "Valuation and fundamental metrics" },
  { name: "Simply Wall St", url: "https://simplywall.st/", note: "Visual company fundamentals" },
  { name: "Nasdaq", url: "https://www.nasdaq.com/", note: "Public-company and market information" }
];


const companies = [
  {id:'abb',name:'ABB',country:'Switzerland',sector:'Industrial technology',description:'Global electrification and automation company.',priorDeals:[{name:'GE Industrial Solutions',year:2018,value:'$2.6B',outcome:'Expanded electrification portfolio'},{name:'ASTI Mobile Robotics',year:2021,value:'Undisclosed',outcome:'Added autonomous mobile robots'}]},
  {id:'rotork',name:'Rotork',country:'United Kingdom',sector:'Industrial technology',description:'Flow-control and instrumentation specialist.',priorDeals:[{name:'Bifold Group',year:2015,value:'£125M',outcome:'Expanded valve-control capabilities'}]},
  {id:'ea',name:'Electronic Arts',country:'United States',sector:'Gaming',description:'Publisher of major sports and entertainment game franchises.',priorDeals:[{name:'Codemasters',year:2021,value:'$1.2B',outcome:'Expanded racing portfolio'},{name:'Glu Mobile',year:2021,value:'$2.1B',outcome:'Added mobile gaming scale'}]},
  {id:'aditya',name:'Aditya Birla Renewables',country:'India',sector:'Renewable energy',description:'Renewable-energy platform within the Aditya Birla Group.',priorDeals:[{name:'Essel Mining renewables portfolio',year:2024,value:'Undisclosed',outcome:'Consolidated clean-energy assets'}]},
  {id:'sprng',name:'Sprng Energy',country:'India',sector:'Renewable energy',description:'Utility-scale renewable power platform.',priorDeals:[]},
  {id:'eqt',name:'EQT',country:'Sweden',sector:'Private equity',description:'Global investment organization focused on active ownership.',priorDeals:[{name:'Baring Private Equity Asia',year:2022,value:'€6.8B',outcome:'Expanded Asian investment platform'}]},
  {id:'kakaku',name:'Kakaku.com',country:'Japan',sector:'Internet services',description:'Operator of digital comparison and restaurant-review platforms.',priorDeals:[]}
];

deals.forEach((d,i)=>{
  d.regulatoryTimeline = d.regulatoryTimeline || [
    {stage:'Announcement',status:'complete',date:d.date},
    {stage:'Board approval',status:'complete',date:'Completed'},
    {stage:'Regulatory review',status:i===2?'complete':'current',date:i===2?'Cleared':'In progress'},
    {stage:'Shareholder vote',status:i===2?'current':'upcoming',date:'Pending'},
    {stage:'Closing',status:'upcoming',date:'Expected later'}
  ];
  d.integrationTimeline = d.integrationTimeline || [
    {stage:'Leadership alignment',status:'upcoming'},
    {stage:'Operating-model design',status:'upcoming'},
    {stage:'Systems integration',status:'upcoming'},
    {stage:'Synergy tracking',status:'upcoming'},
    {stage:'Post-deal review',status:'upcoming'}
  ];
  d.overallScore = Math.round(Object.values(d.scores).reduce((a,b)=>a+b,0)/Object.keys(d.scores).length*10)/10;
});


deals.forEach((d,i)=>{
  d.bullCase=d.bullCase||[d.longTermGoals?.[0]||'Strategic capability expansion','Potential scale and cross-selling benefits','A clearer long-term competitive position'];
  d.bearCase=d.bearCase||['Integration may take longer than expected','The purchase price could limit returns','Cultural or regulatory friction could erode synergies'];
  d.confidence=d.automated?'Discovery only':'Curated research';
  d.premiumPercent=d.premiumPercent??(d.automated?null:[28,22,18,31][i%4]);
});
