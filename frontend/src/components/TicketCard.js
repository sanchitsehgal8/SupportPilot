import React from 'react'

export default function TicketCard({ ticket }){
  return (
    <div className="ticket-card">
      <div className="ticket-header">
        <strong>{ticket.title || ticket.name}</strong>
        <span className={`status ${ticket.status}`}>{ticket.status || 'open'}</span>
      </div>
      <div className="ticket-body">{ticket.description}</div>
      <div className="ticket-footer">
        <small>Priority: {ticket.priority || ticket.predicted_priority || 'medium'}</small>
      </div>
    </div>
  )
}
