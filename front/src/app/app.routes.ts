import { Routes } from '@angular/router';
import { SignUpPageComponent } from './pages/sign-up-page/sign-up-page.component';
import { SignInPageComponent } from './pages/sign-in-page/sign-in-page.component';
import { NotFoundPageComponent } from './pages/not-found-page/not-found-page.component';
import { HomePageComponent } from "./pages/home-page/home-page.component";
import { CustomPageComponent } from "./pages/custom-page/custom-page.component";
import { AccountPageComponent } from "./pages/account-page/account-page.component";
import { FriendsPageComponent } from "./pages/friends-page/friends-page.component";
import { AuthGuard } from "./guards/auth.guard";
import { GuestGuard } from "./guards/guest.guard";
import { EnterGameGuard } from "./guards/enter-game.guard";
import { LeaveGameGuard } from "./guards/leave-game.guard";
import { GamePageComponent } from "./pages/game-page/game-page.component";
import { MonitorPageComponent } from "./pages/monitor-page/monitor-page.component";
import { OnlineGameSelectorPageComponent } from "./pages/online-game-selector-page/online-game-selector-page.component";
import { CreateGamePageComponent } from './pages/create-game-page/create-game-page.component';
import { OauthCallbackComponent } from './components/oauth-callback/oauth-callback.component';

export const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomePageComponent, pathMatch: 'full', canActivate: [AuthGuard] },
  { path: 'account', component: AccountPageComponent, pathMatch: 'full', canActivate: [AuthGuard] },
  { path: 'custom', component: CustomPageComponent, pathMatch: 'full', canActivate: [AuthGuard] },
  { path: 'friends', component: FriendsPageComponent, pathMatch: 'full', canActivate: [AuthGuard] },
  { path: 'local', component: CreateGamePageComponent, pathMatch: 'full', canActivate: [AuthGuard, EnterGameGuard], canDeactivate: [LeaveGameGuard], data: { gameType: 'local' } },
  { path: 'local/waiting', component: MonitorPageComponent, pathMatch: 'full', canActivate: [AuthGuard, EnterGameGuard], canDeactivate: [LeaveGameGuard], data: { gameType: 'local' } },
  { path: 'local/:channel_id/:arena_id', component: GamePageComponent, pathMatch: 'prefix', canActivate: [AuthGuard, EnterGameGuard], canDeactivate: [LeaveGameGuard], data: { gameType: 'local' } },
  { path: 'online', component: OnlineGameSelectorPageComponent, pathMatch: 'full', canActivate: [AuthGuard, EnterGameGuard], canDeactivate: [LeaveGameGuard], data: { gameType: 'online' } },
  { path: 'online/create/options', component: CreateGamePageComponent, pathMatch: 'full', canActivate: [AuthGuard, EnterGameGuard], canDeactivate: [LeaveGameGuard], data: { gameType: 'online' } },
  { path: 'online/create/waiting', component: MonitorPageComponent, pathMatch: 'full', canActivate: [AuthGuard, EnterGameGuard], canDeactivate: [LeaveGameGuard], data: { gameType: 'online', actionType: 'create'} },
  { path: 'online/join', component: MonitorPageComponent, pathMatch: 'full', canActivate: [AuthGuard, EnterGameGuard], canDeactivate: [LeaveGameGuard], data: { gameType: 'online' , actionType: 'join'} },
  { path: 'online/join/:channel_id', component: MonitorPageComponent, pathMatch: 'full', canActivate: [AuthGuard, EnterGameGuard], canDeactivate: [LeaveGameGuard], data: { gameType: 'online', actionType: 'join_specific'} },
  { path: 'online/:channel_id/:arena_id', component: GamePageComponent, pathMatch: 'prefix', canActivate: [AuthGuard, EnterGameGuard], canDeactivate: [LeaveGameGuard], data: { gameType: 'online' } },
  { path: 'oauth-callback', component: OauthCallbackComponent, pathMatch: 'prefix', canActivate: [GuestGuard] },
  { path: 'sign-in', component: SignInPageComponent, pathMatch: 'full', canActivate: [GuestGuard] },
  { path: 'sign-up', component: SignUpPageComponent, pathMatch: 'full', canActivate: [GuestGuard] },
  { path: '404', component: NotFoundPageComponent, pathMatch: 'full' },
  { path: '**', redirectTo: '/404' },
];
