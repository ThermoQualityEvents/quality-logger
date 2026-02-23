from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-me'  # Change this to something random
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quality_events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Quality Event model
class QualityEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    event_type = db.Column(db.String(100), nullable=False)  # e.g., Non-conformance, Incident, Complaint
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(50))  # Low, Medium, High, Critical
    reporter = db.Column(db.String(100))
    actions = db.Column(db.Text)
    status = db.Column(db.String(50), default='Open')  # Open, In Progress, Closed

    def __repr__(self):
        return f'<Event {self.id}: {self.event_type}>'

# Create the database tables (run once)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    events = QualityEvent.query.order_by(QualityEvent.date.desc()).all()
    return render_template('index.html', events=events)

@app.route('/add', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        event_type = request.form['event_type']
        description = request.form['description']
        severity = request.form.get('severity')
        reporter = request.form.get('reporter')
        actions = request.form.get('actions')
        status = request.form.get('status', 'Open')

        new_event = QualityEvent(
            event_type=event_type,
            description=description,
            severity=severity,
            reporter=reporter,
            actions=actions,
            status=status
        )
        db.session.add(new_event)
        db.session.commit()
        flash('Quality event logged successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)





