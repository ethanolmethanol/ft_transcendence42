import { Routes } from '@angular/router';
import { SignUpPageComponent } from './pages/sign-up-page/sign-up-page.component';
import { SignInPageComponent } from './pages/sign-in-page/sign-in-page.component';
import { NotFoundPageComponent } from './pages/not-found-page/not-found-page.component';
import { HomePageComponent } from "./pages/home-page/home-page.component";
import { AuthGuard } from "./guards/auth.guard";
import {GuestGuard} from "./guards/guest.guard";
import {GamePageComponent} from "./pages/game-page/game-page.component";
import {MonitorPageComponent} from "./pages/monitor-page/monitor-page.component";

export const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomePageComponent, pathMatch: 'full', canActivate: [AuthGuard] },
  { path: 'local-game', component: MonitorPageComponent, pathMatch: 'full', canActivate: [AuthGuard] },
  { path: 'local-game/:channel_id/:arena_id', component: GamePageComponent, pathMatch: 'prefix', canActivate: [AuthGuard] },
  { path: 'sign-in', component: SignInPageComponent, pathMatch: 'full', canActivate: [GuestGuard] },
  { path: 'sign-up', component: SignUpPageComponent, pathMatch: 'full', canActivate: [GuestGuard] },
  { path: '404', component: NotFoundPageComponent, pathMatch: 'full' },
  { path: '**', redirectTo: '/404' },
];
