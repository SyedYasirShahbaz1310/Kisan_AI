# Static Files

This directory contains static web assets for the Kisan AI Assistant.

## Files

### ui.html
The main web interface for the Kisan AI Assistant.

**Features**:
- Modern, responsive design
- Chat-style interface
- Language selector (Auto detect, Roman Urdu, Urdu, English)
- Real-time API communication
- Loading states and error handling
- Source attribution display

**Access**: `/static/ui.html` when the Flask app is running

**Technologies**:
- Pure HTML, CSS, and JavaScript
- No external dependencies
- Gradient design with agriculture theme colors

## Customization

You can customize the UI by editing `ui.html`:

### Change Colors
Look for the CSS section and modify:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Change Branding
Update the header text:
```html
<h1>🌾 Kisan AI Assistant</h1>
```

### Add Features
The JavaScript code handles API communication. You can extend it to add:
- Voice input
- Image uploads
- Chat history
- Favorite questions
- etc.

## API Integration

The UI communicates with the Flask backend via:

```javascript
fetch('/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, language })
})
```

Response format:
```json
{
    "answer": "...",
    "sources": ["source1", "source2"],
    "language": "..."
}
```

## Adding More Pages

You can add more HTML pages to this directory:

1. Create a new `.html` file
2. Place it in the `static/` directory
3. Access it at `/static/filename.html`

## Images and Assets

To add images or other assets:

1. Create subdirectories: `static/images/`, `static/css/`, `static/js/`
2. Place files there
3. Reference in HTML: `<img src="/static/images/logo.png">`

## Mobile Responsive

The current UI is mobile-responsive. Test on different screen sizes.

## Browser Compatibility

Works on:
- ✅ Chrome, Edge, Safari, Firefox (latest versions)
- ✅ Mobile browsers (iOS Safari, Chrome Android)
- ⚠️ IE11 not supported (uses modern JavaScript)

---

**Note**: This is a single-page application. For a more complex UI, consider using a framework like React, Vue, or Svelte.
