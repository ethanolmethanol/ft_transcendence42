import { Routes } from '@angular/router';
import { SignUpPageComponent } from './Pages/sign-up-page/sign-up-page.component';
import { SignInPageComponent } from './Pages/sign-in-page/sign-in-page.component';
import { NotFoundPageComponent } from './Pages/not-found-page/not-found-page.component';

export const routes: Routes = [
  { path: '', redirectTo: 'sign-in', pathMatch: 'full' },
  { path: 'sign-in', component: SignInPageComponent, pathMatch: 'full'},
  { path: 'sign-up', component: SignUpPageComponent, pathMatch: 'full'},
  { path: '404', component: NotFoundPageComponent, pathMatch: 'full'},
  { path: '**', redirectTo: '/404' },
];
