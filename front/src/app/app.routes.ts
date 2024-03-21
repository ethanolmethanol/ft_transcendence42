import { Routes } from '@angular/router';
import { SignUpPageComponent } from './Pages/sign-up-page/sign-up-page.component';
import { SignInPageComponent } from './Pages/sign-in-page/sign-in-page.component';
import { NotFoundPageComponent } from './Pages/not-found-page/not-found-page.component';
import {HomePageComponent} from "./Pages/home-page/home-page.component";
import {AuthGuard} from "./guards/auth.guard";
import {RootComponent} from "./components/root/root.component";
// import {GuestGuard} from "./guards/guest.guard";

export const routes: Routes = [
  { path: '', component: RootComponent, pathMatch: 'full', canActivate: [AuthGuard] },
  { path: 'home', component: HomePageComponent, pathMatch: 'full', canActivate: [AuthGuard] },
  { path: 'sign-in', component: SignInPageComponent, pathMatch: 'full' },
  { path: 'sign-up', component: SignUpPageComponent, pathMatch: 'full' },
  { path: '404', component: NotFoundPageComponent, pathMatch: 'full'},
  { path: '**', redirectTo: '/404' },
];
