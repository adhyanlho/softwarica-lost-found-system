from app import create_app

app = create_app()

if __name__ == '__main__':
    # Starts the local development server on port 5000
    app.run(debug=True, host='127.0.0.1', port=5000)

# --- App-Wide Error Handlers ---
@main_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main_bp.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500