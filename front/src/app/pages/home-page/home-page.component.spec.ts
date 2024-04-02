import { HomePageComponent } from './home-page.component';
import {UserService} from "../../services/user/user.service";

describe('HomePageComponent', () => {
  let component: HomePageComponent;
  let userServiceMock: jasmine.SpyObj<UserService>;

  beforeEach(async () => {
    component = new HomePageComponent(userServiceMock);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
