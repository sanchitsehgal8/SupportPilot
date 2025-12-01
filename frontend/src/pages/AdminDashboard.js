import React, { useEffect, useState } from 'react'
import api from '../api/client'
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts'

const COLORS = ['#0088FE', '#00C49F', '#FF8042']

export default function AdminDashboard(){
  const [stats, setStats] = useState(null)

  useEffect(()=>{
    async function load(){
      try{
        const res = await api.get('/analytics/dashboard')
        setStats(res.data.data)
      }catch(e){console.warn(e)}
    }
    load()
  }, [])

  return (
    <div className="page">
      <h2>Admin Dashboard</h2>
      {!stats && <div>Loading...</div>}
      {stats && (
        <div className="charts">
          <div className="chart-card">
            <h4>Sentiment Distribution</h4>
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie dataKey="value" data={[{name:'positive', value: stats.sentiment.positive},{name:'neutral', value: stats.sentiment.neutral},{name:'negative', value: stats.sentiment.negative}]}>
                  {[{name:'positive'},{name:'neutral'},{name:'negative'}].map((entry, idx) => (
                    <Cell key={`cell-${idx}`} fill={COLORS[idx % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-card">
            <h4>Tickets</h4>
            <div>Total: {stats.tickets.total_tickets}</div>
            <div>Open: {stats.tickets.open_tickets}</div>
            <div>In Progress: {stats.tickets.in_progress_tickets}</div>
            <div>Resolved: {stats.tickets.resolved_tickets}</div>
          </div>
        </div>
      )}
    </div>
  )
}
