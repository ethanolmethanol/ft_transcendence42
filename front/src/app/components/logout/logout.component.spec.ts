import { LogoutComponent } from './logout.component';
import { AuthService } from "../../services/auth/auth.service";

describe('LogoutComponent', () => {
  let component: LogoutComponent;
  let authService: AuthService;

  beforeEach(async () => {
    component = new LogoutComponent(authService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
