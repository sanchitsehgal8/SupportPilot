"""Main Flask application"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from datetime import datetime

from backend.config import get_config
from backend.utils.supabase_client import SupabaseClient
from backend.utils.jwt_utils import JWTUtils
from backend.services.ticket_service import TicketService
from backend.services.user_service import UserService
from backend.services.comment_service import CommentService
from backend.services.notification_service import NotificationService
from backend.services.analytics_service import AnalyticsService
from backend.services.assignment_engine import TicketAssignmentEngine
from backend.controllers.auth_controller import AuthController, auth_bp
from backend.controllers.ticket_controller import TicketController, ticket_bp
from backend.controllers.analytics_controller import AnalyticsController, analytics_bp


def create_app():
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    config = get_config()
    app.config.from_object(config)
    
    # Initialize CORS
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    
    # Initialize Supabase
    try:
        supabase = SupabaseClient.get_instance(
            app.config['SUPABASE_URL'],
            app.config['SUPABASE_KEY']
        )
    except Exception as e:
        print(f"Warning: Supabase initialization failed: {e}")
    
    # Initialize services
    try:
        supabase_client = SupabaseClient().get_client()
        ticket_service = TicketService(supabase_client)
        user_service = UserService(supabase_client)
        comment_service = CommentService(supabase_client)
        notification_service = NotificationService(supabase_client)
        analytics_service = AnalyticsService(supabase_client)
        assignment_engine = TicketAssignmentEngine(supabase_client, user_service, analytics_service)
    except Exception as e:
        print(f"Warning: Service initialization failed: {e}")
    
    # Initialize JWT utils
    jwt_utils = JWTUtils(app.config['JWT_SECRET_KEY'])
    
    # Initialize controllers
    auth_controller = AuthController(user_service, jwt_utils)
    ticket_controller = TicketController(ticket_service)
    analytics_controller = AnalyticsController(analytics_service)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(ticket_bp)
    app.register_blueprint(analytics_bp)
    
    # Routes
    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    @app.route('/api/auth/register', methods=['POST'])
    def register():
        """Register endpoint"""
        return auth_controller.register(request.get_json() or {})
    
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        """Login endpoint"""
        return auth_controller.login(request.get_json() or {})
    
    @app.route('/api/tickets', methods=['POST'])
    def create_ticket():
        """Create ticket endpoint"""
        user_id = request.headers.get('X-User-ID')
        if not user_id:
            from backend.utils.error_handler import ErrorHandler
            return ErrorHandler.unauthorized('User ID required')
        return ticket_controller.create_ticket(request.get_json() or {}, user_id)
    
    @app.route('/api/tickets/<ticket_id>', methods=['GET'])
    def get_ticket(ticket_id):
        """Get ticket endpoint"""
        return ticket_controller.get_ticket(ticket_id)
    
    @app.route('/api/tickets/status/<ticket_id>', methods=['PUT'])
    def update_ticket_status(ticket_id):
        """Update ticket status endpoint"""
        return ticket_controller.update_ticket_status(ticket_id, request.get_json() or {})
    
    @app.route('/api/tickets/assign/<ticket_id>', methods=['POST'])
    def assign_ticket(ticket_id):
        """Assign ticket endpoint"""
        return ticket_controller.assign_ticket(ticket_id, request.get_json() or {})
    
    @app.route('/api/analytics/dashboard', methods=['GET'])
    def get_dashboard():
        """Dashboard stats endpoint"""
        return analytics_controller.get_dashboard_stats()
    
    @app.route('/api/analytics/agents/<agent_id>', methods=['GET'])
    def get_agent_perf(agent_id):
        """Agent performance endpoint"""
        return analytics_controller.get_agent_performance(agent_id)
    
    @app.route('/api/analytics/agents', methods=['GET'])
    def get_all_agents():
        """All agents performance endpoint"""
        return analytics_controller.get_all_agents_performance()
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({
            'success': False,
            'error': 'Not found',
            'error_code': 'NOT_FOUND'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'error_code': 'INTERNAL_ERROR'
        }), 500
    
    return app


# Create app instance
app = create_app()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
