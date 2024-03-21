import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import {AuthService} from "../../services/auth/auth.service";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [],
  templateUrl: './root.component.html',
  styleUrl: './root.component.css'
})
export class RootComponent implements OnInit {

  constructor(private authService: AuthService, private router: Router) {}
  ngOnInit() {
    this.router.navigate(['/home']);
  }
}
