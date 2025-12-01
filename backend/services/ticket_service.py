"""Ticket Service - handles ticket business logic"""
from typing import List, Dict, Optional
from datetime import datetime
from backend.models.ticket import Ticket


class TicketService:
    """Service class for ticket operations"""
    
    def __init__(self, db):
        self.db = db
        
    def create_ticket(self, customer_id: str, title: str, description: str,
                     priority: str = "medium") -> Dict:
        """Create a new ticket"""
        try:
            ticket_data = {
                'customer_id': customer_id,
                'title': title,
                'description': description,
                'priority': priority,
                'status': 'open',
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            result = self.db.table('tickets').insert(ticket_data).execute()
            return {'success': True, 'data': result.data[0] if result.data else ticket_data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_ticket(self, ticket_id: str) -> Optional[Dict]:
        """Get ticket by ID"""
        try:
            result = self.db.table('tickets').select('*').eq('ticket_id', ticket_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            return None
    
    def get_customer_tickets(self, customer_id: str) -> List[Dict]:
        """Get all tickets for a customer"""
        try:
            result = self.db.table('tickets').select('*').eq('customer_id', customer_id).execute()
            return result.data if result.data else []
        except Exception as e:
            return []
    
    def get_agent_tickets(self, agent_id: str) -> List[Dict]:
        """Get all assigned tickets for an agent"""
        try:
            result = self.db.table('tickets').select('*').eq('assigned_agent_id', agent_id).execute()
            return result.data if result.data else []
        except Exception as e:
            return []
    
    def update_ticket_status(self, ticket_id: str, status: str) -> Dict:
        """Update ticket status"""
        try:
            update_data = {
                'status': status,
                'updated_at': datetime.utcnow().isoformat()
            }
            result = self.db.table('tickets').update(update_data).eq('ticket_id', ticket_id).execute()
            return {'success': True, 'data': result.data[0] if result.data else update_data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def assign_ticket(self, ticket_id: str, agent_id: str) -> Dict:
        """Assign ticket to an agent"""
        try:
            update_data = {
                'assigned_agent_id': agent_id,
                'status': 'in_progress',
                'updated_at': datetime.utcnow().isoformat()
            }
            result = self.db.table('tickets').update(update_data).eq('ticket_id', ticket_id).execute()
            return {'success': True, 'data': result.data[0] if result.data else update_data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_all_tickets(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get all tickets with pagination"""
        try:
            result = self.db.table('tickets').select('*').range(offset, offset + limit - 1).execute()
            return result.data if result.data else []
        except Exception as e:
            return []
