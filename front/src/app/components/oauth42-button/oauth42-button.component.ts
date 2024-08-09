import { Component, Input } from '@angular/core';
import { AuthService } from '../../services/auth/auth.service';

@Component({
  selector: 'app-oauth42-button',
  standalone: true,
  imports: [],
  templateUrl: './oauth42-button.component.html',
  styleUrl: './oauth42-button.component.css'
})
export class Oauth42ButtonComponent {
  @Input() text: string = "";

  constructor(private authService: AuthService) {}

  public navigate_to_42_api(): void {
    this.authService.authorize42().subscribe( {
      next: url => {
        window.open(url, '_self');
      }
    });
  }
}
