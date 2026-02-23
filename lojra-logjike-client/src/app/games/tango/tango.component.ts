import { Component } from '@angular/core';

@Component({
  selector: 'app-tango',
  standalone: true,
  template: `
    <div class="placeholder">
      <svg width="80" height="80" viewBox="0 0 64 64">
        <rect x="6" y="6" width="24" height="24" rx="4" fill="#FFF7ED" stroke="#1a1a1a" stroke-width="2"/>
        <rect x="34" y="6" width="24" height="24" rx="4" fill="#FDBA74" stroke="#1a1a1a" stroke-width="2"/>
        <rect x="6" y="34" width="24" height="24" rx="4" fill="#FDBA74" stroke="#1a1a1a" stroke-width="2"/>
        <rect x="34" y="34" width="24" height="24" rx="4" fill="#FFF7ED" stroke="#1a1a1a" stroke-width="2"/>
        <line x1="31" y1="15" x2="33" y2="15" stroke="#F97316" stroke-width="2.5" stroke-linecap="round"/>
        <line x1="31" y1="19" x2="33" y2="19" stroke="#F97316" stroke-width="2.5" stroke-linecap="round"/>
        <line x1="30.5" y1="43" x2="33.5" y2="49" stroke="#E11D48" stroke-width="2.5" stroke-linecap="round"/>
        <line x1="33.5" y1="43" x2="30.5" y2="49" stroke="#E11D48" stroke-width="2.5" stroke-linecap="round"/>
      </svg>
      <h2>Tango</h2>
      <p>Se shpejti...</p>
    </div>
  `,
  styles: [`.placeholder{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;padding:48px 24px}h2{font-family:var(--font-display);font-size:1.6rem;font-weight:900}p{color:#888;font-weight:600;font-size:1.1rem}`]
})
export class TangoComponent {}
