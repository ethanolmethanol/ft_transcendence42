import { Routes } from '@angular/router';
import { SignUpPageComponent } from './Pages/sign-up-page/sign-up-page.component';
import { SignInPageComponent } from './Pages/sign-in-page/sign-in-page.component';
import { NotFoundPageComponent } from './Pages/not-found-page/not-found-page.component';
import { HomePageComponent } from "./Pages/home-page/home-page.component";
import { AuthGuard } from "./guards/auth.guard";

export const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomePageComponent, canActivate: [AuthGuard] },
  { path: 'sign-in', component: SignInPageComponent },
  { path: 'sign-up', component: SignUpPageComponent },
  { path: '404', component: NotFoundPageComponent, pathMatch: 'full' },
  { path: '**', redirectTo: '/404' },
];
