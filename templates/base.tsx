import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export default function Component() {
  const [showLogin, setShowLogin] = useState(false)
  const [showRegister, setShowRegister] = useState(false)

  return (
    <div className="min-h-screen bg-pink-100 flex flex-col items-center justify-center p-4 lg:p-8" style={{
      backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23f472b6' fill-opacity='0.2'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
      imageRendering: 'pixelated'
    }}>
      <div className="fixed top-4 left-4 lg:top-8 lg:left-8">
        <div className="w-12 h-12 lg:w-16 lg:h-16 bg-pink-500 rounded-lg overflow-hidden" style={{imageRendering: 'pixelated'}}>
          <img src="/placeholder.svg?height=64&width=64" alt="Pixel Art Avatar" className="w-full h-full object-cover" />
        </div>
      </div>

      <div className="bg-white p-6 lg:p-8 rounded-lg shadow-lg max-w-md w-full mb-8" style={{
        borderImage: 'url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAYAAACp8Z5+AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAIGNIUk0AAHolAACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAAAZSURBVHjaYmBgYNBhYGBQBmImBjQAEGAABEgBDTMYuTUAAAAASUVORK5CYII=") 2',
        borderStyle: 'solid',
        borderWidth: '4px',
        imageRendering: 'pixelated'
      }}>
        <h2 className="text-2xl lg:text-3xl font-bold mb-4 text-center text-pink-600" style={{fontFamily: '"Press Start 2P", cursive'}}>公告栏</h2>
        <p className="mb-4 text-gray-600 text-sm lg:text-base" style={{fontFamily: 'monospace', imageRendering: 'pixelated'}}>欢迎来到像素聊天平台！我们正在进行系统升级，敬请期待更多精彩功能。现在支持电脑和手机访问，界面会自动适应您的设备。</p>
      </div>

      <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
        <Button
          onClick={() => setShowLogin(true)}
          className="bg-pink-500 hover:bg-pink-600 text-white font-bold py-2 px-4 w-full sm:w-auto"
          style={{
            fontFamily: '"Press Start 2P", cursive',
            imageRendering: 'pixelated',
            boxShadow: '0 4px 0 #d53f8c'
          }}
        >
          登录
        </Button>
        <Button
          onClick={() => setShowRegister(true)}
          className="bg-purple-500 hover:bg-purple-600 text-white font-bold py-2 px-4 w-full sm:w-auto"
          style={{
            fontFamily: '"Press Start 2P", cursive',
            imageRendering: 'pixelated',
            boxShadow: '0 4px 0 #805ad5'
          }}
        >
          注册
        </Button>
      </div>

      {showLogin && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-white p-6 lg:p-8 rounded-lg w-full max-w-md" style={{
            borderImage: 'url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAYAAACp8Z5+AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAIGNIUk0AAHolAACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAAAZSURBVHjaYmBgYNBhYGBQBmImBjQAEGAABEgBDTMYuTUAAAAASUVORK5CYII=") 2',
            borderStyle: 'solid',
            borderWidth: '4px',
            imageRendering: 'pixelated'
          }}>
            <h2 className="text-2xl font-bold mb-4 text-pink-600" style={{fontFamily: '"Press Start 2P", cursive'}}>登录</h2>
            <form className="space-y-4">
              <div>
                <Label htmlFor="username" className="block text-sm font-medium text-gray-700" style={{fontFamily: 'monospace'}}>用户名</Label>
                <Input type="text" id="username" name="username" required className="mt-1 block w-full" style={{fontFamily: 'monospace', imageRendering: 'pixelated'}} />
              </div>
              <div>
                <Label htmlFor="password" className="block text-sm font-medium text-gray-700" style={{fontFamily: 'monospace'}}>密码</Label>
                <Input type="password" id="password" name="password" required className="mt-1 block w-full" style={{fontFamily: 'monospace', imageRendering: 'pixelated'}} />
              </div>
              <Button type="submit" className="w-full bg-pink-500 hover:bg-pink-600 text-white font-bold py-2 px-4" style={{fontFamily: '"Press Start 2P", cursive', imageRendering: 'pixelated', boxShadow: '0 4px 0 #d53f8c'}}>
                登录
              </Button>
            </form>
            <Button onClick={() => setShowLogin(false)} className="mt-4 w-full bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4" style={{fontFamily: '"Press Start 2P", cursive', imageRendering: 'pixelated', boxShadow: '0 4px 0 #a0aec0'}}>
              关闭
            </Button>
          </div>
        </div>
      )}

      {showRegister && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-white p-6 lg:p-8 rounded-lg w-full max-w-md" style={{
            borderImage: 'url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAYAAACp8Z5+AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAIGNIUk0AAHolAACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAAAZSURBVHjaYmBgYNBhYGBQBmImBjQAEGAABEgBDTMYuTUAAAAASUVORK5CYII=") 2',
            borderStyle: 'solid',
            borderWidth: '4px',
            imageRendering: 'pixelated'
          }}>
            <h2 className="text-2xl font-bold mb-4 text-purple-600" style={{fontFamily: '"Press Start 2P", cursive'}}>注册</h2>
            <form className="space-y-4">
              <div>
                <Label htmlFor="newUsername" className="block text-sm font-medium text-gray-700" style={{fontFamily: 'monospace'}}>用户名</Label>
                <Input type="text" id="newUsername" name="newUsername" required className="mt-1 block w-full" style={{fontFamily: 'monospace', imageRendering: 'pixelated'}} />
              </div>
              <div>
                <Label htmlFor="newPassword" className="block text-sm font-medium text-gray-700" style={{fontFamily: 'monospace'}}>密码</Label>
                <Input type="password" id="newPassword" name="newPassword" required className="mt-1 block w-full" style={{fontFamily: 'monospace', imageRendering: 'pixelated'}} />
              </div>
              <div>
                <Label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700" style={{fontFamily: 'monospace'}}>确认密码</Label>
                <Input type="password" id="confirmPassword" name="confirmPassword" required className="mt-1 block w-full" style={{fontFamily: 'monospace', imageRendering: 'pixelated'}} />
              </div>
              <Button type="submit" className="w-full bg-purple-500 hover:bg-purple-600 text-white font-bold py-2 px-4" style={{fontFamily: '"Press Start 2P", cursive', imageRendering: 'pixelated', boxShadow: '0 4px 0 #805ad5'}}>
                注册
              </Button>
            </form>
            <Button onClick={() => setShowRegister(false)} className="mt-4 w-full bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4" style={{fontFamily: '"Press Start 2P", cursive', imageRendering: 'pixelated', boxShadow: '0 4px 0 #a0aec0'}}>
              关闭
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}