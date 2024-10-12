import 'package:flutter/material.dart';
import 'home.dart';

class LandingPage extends StatefulWidget {
  @override
  _LandingPageState createState() => _LandingPageState();
}

class _LandingPageState extends State<LandingPage>
    with TickerProviderStateMixin {
  double _slideOffset = 0.0;

  @override
  void initState() {
    super.initState();
    // Set a timer to slide off the image after 1.5 seconds
    Future.delayed(const Duration(seconds: 1), () {
      setState(() {
        _slideOffset =
            MediaQuery.of(context).size.width; // Slide off the screen
      });
      // Navigate to the home page after the animation
      Future.delayed(const Duration(milliseconds: 500), () {
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(
              builder: (context) => MyHomePage(title: 'Recycletron')),
        );
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          SlideTransition(
            position: Tween<Offset>(
              begin: Offset.zero,
              end: Offset(1.0, 0.0), // Slide out to the right
            ).animate(CurvedAnimation(
              parent: AnimationController(
                duration: const Duration(milliseconds: 500),
                vsync: this,
              )..forward(), // Start the animation immediately
              curve: Curves.easeInOut,
            )),
            child: Center(
              child: Image.asset(
                'assets/recycleLogo.pg', // Update with your asset path
                fit: BoxFit.cover,
                width: double.infinity,
                height: double.infinity,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
