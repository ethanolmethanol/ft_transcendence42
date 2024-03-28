import { LogoutComponent } from './logout.component';
import { AuthService } from "../../services/auth/auth.service";

describe('LogoutComponent', () => {
  let component: LogoutComponent;
  let authService: AuthService;

  beforeEach(async () => {
    authService = jasmine.createSpyObj('AuthService', ['logout']);
    component = new LogoutComponent(authService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call logout method of AuthService when logOut is called', () => {
    component.logOut();
    expect(authService.logout).toHaveBeenCalled();
  });
});
