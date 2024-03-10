import { Routes } from '@angular/router';
import {SignInComponent} from "./Pages/sign-in-page/sign-in/sign-in.component";

export const routes: Routes = [
  { path: '', component: SignInComponent },
  { path: 'sign-in', component: SignInComponent },
  // { path: 'sign-up', component: SignUpComponent },
  // { path: '404', component: NotFoundComponent },
  { path: '**', redirectTo: '/404' }
];
