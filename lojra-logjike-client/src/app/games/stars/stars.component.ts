import { Component } from '@angular/core';
@Component({
  selector: 'app-stars',
  standalone: true,
  template: `
    <div class="placeholder">
      <svg width="80" height="80" viewBox="0 0 64 64"><polygon points="32,4 39,24 60,24 43,37 49,58 32,45 15,58 21,37 4,24 25,24" fill="#F59E0B" stroke="#1a1a1a" stroke-width="2"/></svg>
      <h2>Stars</h2>
      <p>Se shpejti...</p>
    </div>
  `,
  styles: [`.placeholder{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;padding:48px 24px}h2{font-family:var(--font-display);font-size:1.6rem;font-weight:900}p{color:#888;font-weight:600;font-size:1.1rem}`]
})
export class StarsComponent {}
