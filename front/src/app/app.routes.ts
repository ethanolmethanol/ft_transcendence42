import { Routes } from '@angular/router';
import { SignUpPageComponent } from './pages/sign-up-page/sign-up-page.component';
import { SignInPageComponent } from './pages/sign-in-page/sign-in-page.component';
import { NotFoundPageComponent } from './pages/not-found-page/not-found-page.component';
import { HomePageComponent } from "./pages/home-page/home-page.component";
import { AuthGuard } from "./guards/auth.guard";
import {GuestGuard} from "./guards/guest.guard";

export const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomePageComponent, pathMatch: 'full', canActivate: [AuthGuard] },
  { path: 'sign-in', component: SignInPageComponent, pathMatch: 'full', canActivate: [GuestGuard] },
  { path: 'sign-up', component: SignUpPageComponent, pathMatch: 'full', canActivate: [GuestGuard] },
  { path: '404', component: NotFoundPageComponent, pathMatch: 'full' },
  { path: '**', redirectTo: '/404' },
];
