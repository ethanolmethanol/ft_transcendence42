import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../../services/auth/auth.service';

@Component({
  selector: 'app-oauth-callback',
  standalone: true,
  imports: [],
  templateUrl: './oauth-callback.component.html',
  styleUrl: './oauth-callback.component.css'
})
export class OauthCallbackComponent implements OnInit {

  constructor(
    private route: ActivatedRoute,
    private authService: AuthService,
    private router: Router,
  ) {}
  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      const code = params["code"];
      if (code) {
        console.log("Code received: ", code);
        this.authService.exchangeCodeForToken(code).subscribe({
          next: () => {
            this.router.navigate(["/home"]);
          },
          error: (err): void => {
            console.error("Error exchanging code", err);
          }
        });
      } else {
        console.error("No code received");
      }
    });
  }
}
