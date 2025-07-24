import { Calculator, Activity, TrendingUp, BarChart3, Target, Zap } from 'lucide-react'

const DashboardHome = ({ setActiveTab }) => {
  const features = [
    {
      id: 'capm',
      title: 'CAPM Calculator',
      description: 'Calculate Beta and Expected Returns using the Capital Asset Pricing Model. Analyze stock performance against market benchmarks.',
      icon: Calculator,
      color: 'bg-blue-500',
      stats: 'Risk Analysis'
    },
    {
      id: 'analysis',
      title: 'Stock Analysis',
      description: 'Comprehensive technical analysis with indicators, price trends, and volume analysis for informed decision making.',
      icon: Activity,
      color: 'bg-green-500',
      stats: 'Technical Indicators'
    },
    {
      id: 'prediction',
      title: 'Stock Prediction',
      description: 'Predict future stock prices using ARIMA models. Get 30-day forecasts with confidence intervals.',
      icon: TrendingUp,
      color: 'bg-purple-500',
      stats: 'ARIMA Forecasting'
    }
  ]

  const stats = [
    { name: 'Market Coverage', value: 'Global', icon: Target },
    { name: 'Real-time Data', value: 'Live', icon: Zap },
    { name: 'Analysis Tools', value: '3+', icon: BarChart3 },
  ]

  return (
    <div className="space-y-4 lg:space-y-6 xl:space-y-8">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-green-500 via-emerald-500 to-teal-500 rounded-2xl shadow-2xl p-6 lg:p-8 xl:p-10 text-white relative overflow-hidden">
        <div className="absolute inset-0 bg-white/10 backdrop-blur-sm"></div>
        <div className="max-w-none xl:max-w-5xl">
          <h1 className="relative text-3xl lg:text-4xl xl:text-5xl font-bold mb-2 lg:mb-4 drop-shadow-lg">Welcome to Stocklyzer</h1>
          <p className="relative text-green-100 text-lg lg:text-xl xl:text-2xl max-w-4xl drop-shadow-md">
            Your comprehensive stock analysis and prediction platform. Forecast the future, analyze the past, and make smarter investment decisions.
          </p>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 lg:gap-6 xl:gap-8">
        {stats.map((stat) => {
          const Icon = stat.icon
          return (
            <div key={stat.name} className="bg-white rounded-xl shadow-lg border border-green-200 p-6 hover:shadow-xl transition-all duration-300 hover:scale-105">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="p-3 bg-gradient-to-br from-green-400 to-emerald-500 rounded-xl shadow-lg">
                    <Icon className="h-6 w-6 text-white" />
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                  <p className="text-2xl font-bold text-gray-800">{stat.value}</p>
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 lg:gap-6 xl:gap-8">
        {features.map((feature) => {
          const Icon = feature.icon
          return (
            <div
              key={feature.id}
              className="bg-white rounded-xl shadow-lg border border-green-200 hover:shadow-2xl hover:border-green-300 transition-all duration-300 cursor-pointer transform hover:scale-105 group"
              onClick={() => setActiveTab(feature.id)}
            >
              <div className="p-6">
                <div className="flex items-center mb-4">
                  <div className={`${feature.color} rounded-xl p-3 shadow-lg group-hover:shadow-xl transition-shadow`}>
                    <Icon className="h-6 w-6 text-white" />
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-bold text-gray-800 group-hover:text-green-700 transition-colors">{feature.title}</h3>
                    <p className="text-sm text-gray-600 font-medium">{feature.stats}</p>
                  </div>
                </div>
                <p className="text-gray-700 mb-4 leading-relaxed">{feature.description}</p>
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    setActiveTab(feature.id)
                  }}
                  className="w-full bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white font-semibold py-3 px-4 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105"
                >
                  Get Started
                </button>
              </div>
            </div>
          )
        })}
      </div>

      {/* Quick Start Guide */}
      <div className="bg-white rounded-xl shadow-lg border border-green-200 p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-6">Quick Start Guide</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 lg:gap-6 xl:gap-8">
          <div className="text-center">
            <div className="bg-gradient-to-br from-green-400 to-emerald-500 rounded-full w-14 h-14 flex items-center justify-center mx-auto mb-4 shadow-lg">
              <span className="text-white font-bold text-lg">1</span>
            </div>
            <h3 className="font-bold text-gray-800 mb-2">Choose Your Tool</h3>
            <p className="text-sm text-gray-600 leading-relaxed">Select from CAPM Calculator, Stock Analysis, or Stock Prediction based on your needs.</p>
          </div>
          <div className="text-center">
            <div className="bg-gradient-to-br from-emerald-400 to-teal-500 rounded-full w-14 h-14 flex items-center justify-center mx-auto mb-4 shadow-lg">
              <span className="text-white font-bold text-lg">2</span>
            </div>
            <h3 className="font-bold text-gray-800 mb-2">Enter Stock Symbol</h3>
            <p className="text-sm text-gray-600 leading-relaxed">Input the stock ticker symbol (e.g., AAPL, GOOGL) or search by company name.</p>
          </div>
          <div className="text-center">
            <div className="bg-gradient-to-br from-teal-400 to-cyan-500 rounded-full w-14 h-14 flex items-center justify-center mx-auto mb-4 shadow-lg">
              <span className="text-white font-bold text-lg">3</span>
            </div>
            <h3 className="font-bold text-gray-800 mb-2">Analyze Results</h3>
            <p className="text-sm text-gray-600 leading-relaxed">View interactive charts, technical indicators, and predictions to make informed decisions.</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DashboardHome
